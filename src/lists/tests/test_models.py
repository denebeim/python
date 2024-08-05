from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from lists.models import Item, List

User = get_user_model()


class ListModelTest(TestCase):
    def test_get_absolute_url(self):
        mylist = List.objects.create()
        self.assertEqual(mylist.get_absolute_url(), f"/lists/{mylist.id}/")

    def test_lists_can_have_owners(self):
        user = User.objects.create(email="a@b.com")
        list_ = List.objects.create(owner=user)
        self.assertIn(list_, user.list_set.all())

    def test_list_owner_is_optional(self):
        List.objects.create()  # should not raise

    def test_list_can_be_shared(self):
        user: AbstractUser = User.objects.create(email="c@d.com")
        list_: List = List.objects.create()
        list_.shared_with.add(user.email)
        self.assertIn(user, list_.shared_with.all())


class ItemModelTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/lists/new", data={"text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"text": "A new list item"})
        new_list = List.objects.get()
        self.assertRedirects(response, f"/lists/{new_list.id}/")

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/",
            data={"text": "A new item for an existing list"},
        )
        self.assertRedirects(response, f"/lists/{correct_list.id}/")


class TestModels(TestCase):
    def test_cannot_save_empty_list_items(self):
        mylist = List.objects.create()
        item = Item(list=mylist, text="")
        with self.assertRaises(ValidationError):
            item.full_clean()
            item.save()

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, "")

    def test_item_is_related_to_list(self):
        mylist = List.objects.create()
        item = Item()
        item.list = mylist
        item.save()
        self.assertIn(item, mylist.item_set.all())

    def test_duplicate_items_are_invalid(self):
        mylist = List.objects.create()
        Item.objects.create(list=mylist, text="blah")
        with self.assertRaises(ValidationError):
            item = Item(list=mylist, text="blah")
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text="blah")
        item = Item(list=list2, text="blah")
        item.full_clean()  # should not raise
