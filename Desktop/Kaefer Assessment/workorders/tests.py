from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import ScaffoldComponent
from .forms import ScaffoldComponentForm

class ScaffoldComponentModelTest(TestCase):
    def setUp(self):
        self.component_data = {
            'asset_code': 'ASSET001',
            'name': 'Test Tube',
            'category': 'Tube',
            'weight_kg': 10.50,
            'site': 'Secunda',
            'last_inspection': timezone.now().date(),
            'next_inspection': (timezone.now() + timedelta(days=30)).date(),
        }

    def test_create_scaffold_component(self):
        component = ScaffoldComponent.objects.create(**self.component_data)
        self.assertEqual(component.asset_code, 'ASSET001')
        self.assertEqual(component.name, 'Test Tube')
        self.assertEqual(component.category, 'Tube')
        self.assertEqual(float(component.weight_kg), 10.50)

    def test_weight_kg_validation(self):
        invalid_data = self.component_data.copy()
        invalid_data['weight_kg'] = 0
        with self.assertRaisesRegex(Exception, 'Weight \(kg\) must be greater than 0.'):
            component = ScaffoldComponent.objects.create(**invalid_data)
            component.full_clean() # Manually call full_clean as save() calls it

    def test_length_mm_validation(self):
        invalid_data_low = self.component_data.copy()
        invalid_data_low['length_mm'] = 0
        with self.assertRaisesRegex(Exception, 'Length \(mm\) must be between 1 and 6000.'):
            component = ScaffoldComponent.objects.create(**invalid_data_low)
            component.full_clean()

        invalid_data_high = self.component_data.copy()
        invalid_data_high['length_mm'] = 6001
        with self.assertRaisesRegex(Exception, 'Length \(mm\) must be between 1 and 6000.'):
            component = ScaffoldComponent.objects.create(**invalid_data_high)
            component.full_clean()

    def test_next_inspection_date_validation(self):
        invalid_data = self.component_data.copy()
        invalid_data['next_inspection'] = (timezone.now() - timedelta(days=1)).date()
        with self.assertRaisesRegex(Exception, 'Next inspection date must be on or after the last inspection date.'):
            component = ScaffoldComponent.objects.create(**invalid_data)
            component.full_clean()

    def test_unique_asset_code_site_constraint(self):
        ScaffoldComponent.objects.create(**self.component_data)
        duplicate_data = self.component_data.copy()
        duplicate_data['name'] = 'Another Name' # Change other field to ensure it's the unique constraint
        with self.assertRaisesRegex(Exception, 'already exists'):
            component = ScaffoldComponent.objects.create(**duplicate_data)
            component.full_clean()

class ScaffoldComponentFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'asset_code': 'FORM001',
            'name': 'Form Test Board',
            'category': 'Board',
            'length_mm': 1200,
            'weight_kg': 5.00,
            'condition': 'GOOD',
            'site': 'Sasolburg',
            'location': 'Warehouse',
            'last_inspection': timezone.now().date(),
            'next_inspection': (timezone.now() + timedelta(days=60)).date(),
            'is_in_use': True,
        }

    def test_form_valid_data(self):
        form = ScaffoldComponentForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), form.errors.as_json())

    def test_form_invalid_weight_kg(self):
        invalid_data = self.valid_data.copy()
        invalid_data['weight_kg'] = 0
        form = ScaffoldComponentForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('weight_kg', form.errors)

    def test_form_invalid_length_mm(self):
        invalid_data = self.valid_data.copy()
        invalid_data['length_mm'] = 7000
        form = ScaffoldComponentForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('length_mm', form.errors)

    def test_form_invalid_next_inspection_date(self):
        invalid_data = self.valid_data.copy()
        invalid_data['next_inspection'] = (timezone.now() - timedelta(days=1)).date()
        form = ScaffoldComponentForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('next_inspection', form.errors)

    def test_form_unique_together_asset_code_site(self):
        ScaffoldComponent.objects.create(**self.valid_data)
        duplicate_data = self.valid_data.copy()
        duplicate_data['name'] = 'Another Board' # Change other field
        form = ScaffoldComponentForm(data=duplicate_data)
        self.assertFalse(form.is_valid())
        self.assertIn('asset_code', form.errors)


class ScaffoldComponentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.component1 = ScaffoldComponent.objects.create(
            asset_code='VIEW001', name='Tube A', category='Tube', weight_kg=12.0,
            site='Secunda', last_inspection=timezone.now().date(),
            next_inspection=(timezone.now() + timedelta(days=30)).date(),
            condition='GOOD', is_in_use=False
        )
        self.component2 = ScaffoldComponent.objects.create(
            asset_code='VIEW002', name='Board X', category='Board', weight_kg=8.0,
            site='Sasolburg', last_inspection=timezone.now().date(),
            next_inspection=(timezone.now() + timedelta(days=60)).date(),
            condition='NEW', is_in_use=True
        )
        self.component3 = ScaffoldComponent.objects.create(
            asset_code='VIEW003', name='Tube B', category='Tube', weight_kg=15.0,
            site='Secunda', last_inspection=timezone.now().date(),
            next_inspection=(timezone.now() + timedelta(days=90)).date(),
            condition='REPAIR', is_in_use=True
        )

    def test_list_view(self):
        response = self.client.get(reverse('scaffold_component_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.component1.name)
        self.assertContains(response, self.component2.name)
        self.assertEqual(response.context['page_obj'].paginator.count, 3) # Check total items

    def test_list_view_filter_by_site(self):
        response = self.client.get(reverse('scaffold_component_list'), {'site': 'Secunda'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.component1.name)
        self.assertNotContains(response, self.component2.name)
        self.assertEqual(response.context['page_obj'].paginator.count, 2)

    def test_list_view_filter_by_category(self):
        response = self.client.get(reverse('scaffold_component_list'), {'category': 'Board'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.component1.name)
        self.assertContains(response, self.component2.name)
        self.assertEqual(response.context['page_obj'].paginator.count, 1)

    def test_list_view_filter_by_condition(self):
        response = self.client.get(reverse('scaffold_component_list'), {'condition': 'NEW'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.component1.name)
        self.assertContains(response, self.component2.name)
        self.assertEqual(response.context['page_obj'].paginator.count, 1)

    def test_list_view_filter_by_q_name(self):
        response = self.client.get(reverse('scaffold_component_list'), {'q': 'Board'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.component1.name)
        self.assertContains(response, self.component2.name)
        self.assertEqual(response.context['page_obj'].paginator.count, 1)

    def test_list_view_filter_by_q_asset_code(self):
        response = self.client.get(reverse('scaffold_component_list'), {'q': 'VIEW003'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.component1.name)
        self.assertContains(response, self.component3.name)
        self.assertEqual(response.context['page_obj'].paginator.count, 1)
    
    def test_list_view_filter_by_in_use(self):
        response = self.client.get(reverse('scaffold_component_list'), {'in_use': 'true'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.component1.name)
        self.assertContains(response, self.component2.name)
        self.assertContains(response, self.component3.name)
        self.assertEqual(response.context['page_obj'].paginator.count, 2)

    def test_create_view_get(self):
        response = self.client.get(reverse('scaffold_component_create'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ScaffoldComponentForm)

    def test_create_view_post_valid(self):
        new_data = {
            'asset_code': 'NEW001',
            'name': 'New Coupler',
            'category': 'Coupler',
            'weight_kg': 2.5,
            'site': 'Secunda',
            'last_inspection': timezone.now().date(),
            'next_inspection': (timezone.now() + timedelta(days=100)).date(),
            'condition': 'NEW',
            'is_in_use': False,
        }
        response = self.client.post(reverse('scaffold_component_create'), new_data)
        self.assertEqual(response.status_code, 302) # Redirect on success
        self.assertTrue(ScaffoldComponent.objects.filter(asset_code='NEW001').exists())

    def test_create_view_post_invalid(self):
        invalid_data = {
            'asset_code': 'INVALID001',
            'name': 'Invalid Component',
            'category': 'Tube',
            'weight_kg': 0, # Invalid weight
            'site': 'Secunda',
            'last_inspection': timezone.now().date(),
            'next_inspection': (timezone.now() + timedelta(days=100)).date(),
            'condition': 'NEW',
            'is_in_use': False,
        }
        response = self.client.post(reverse('scaffold_component_create'), invalid_data)
        self.assertEqual(response.status_code, 200) # Form redisplayed with errors
        # Manually check form errors instead of using assertFormError
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('weight_kg', form.errors)
        self.assertIn('Weight (kg) must be greater than 0.', form.errors['weight_kg'])

    def test_detail_view(self):
        response = self.client.get(reverse('scaffold_component_detail', args=[self.component1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.component1.name)
        self.assertContains(response, self.component1.asset_code)

    def test_edit_view_get(self):
        response = self.client.get(reverse('scaffold_component_edit', args=[self.component1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ScaffoldComponentForm)
        self.assertEqual(response.context['form'].instance, self.component1)

    def test_edit_view_post_valid(self):
        updated_data = {
            'asset_code': self.component1.asset_code,
            'name': 'Updated Tube A',
            'category': 'Tube',
            'weight_kg': 13.0,
            'site': self.component1.site,
            'last_inspection': self.component1.last_inspection,
            'next_inspection': self.component1.next_inspection,
            'condition': 'GOOD',
            'is_in_use': True,
        }
        response = self.client.post(reverse('scaffold_component_edit', args=[self.component1.pk]), updated_data)
        self.assertEqual(response.status_code, 302) # Redirect on success
        self.component1.refresh_from_db()
        self.assertEqual(self.component1.name, 'Updated Tube A')
        self.assertTrue(self.component1.is_in_use)

    def test_edit_view_post_invalid(self):
        invalid_updated_data = {
            'asset_code': self.component1.asset_code,
            'name': 'Invalid Update',
            'category': 'Tube',
            'weight_kg': 0, # Invalid weight
            'site': self.component1.site,
            'last_inspection': self.component1.last_inspection,
            'next_inspection': self.component1.next_inspection,
            'condition': 'GOOD',
            'is_in_use': False,
        }
        response = self.client.post(reverse('scaffold_component_edit', args=[self.component1.pk]), invalid_updated_data)
        self.assertEqual(response.status_code, 200) # Form redisplayed with errors
        # Manually check form errors instead of using assertFormError
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('weight_kg', form.errors)
        self.assertIn('Weight (kg) must be greater than 0.', form.errors['weight_kg'])

    def test_delete_view_get(self):
        response = self.client.get(reverse('scaffold_component_delete', args=[self.component1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Are you sure you want to delete')

    def test_delete_view_post(self):
        component_pk = self.component1.pk
        response = self.client.post(reverse('scaffold_component_delete', args=[component_pk]))
        self.assertEqual(response.status_code, 302) # Redirect on success
        self.assertFalse(ScaffoldComponent.objects.filter(pk=component_pk).exists())