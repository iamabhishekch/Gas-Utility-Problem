import os
import django
import random
from datetime import timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gas_utility_service.settings')
django.setup()

# Import models
from django.contrib.auth.models import User
from django.utils import timezone
from customer.models import Customer
from service_requests.models import ServiceRequestType, ServiceRequest
from support_portal.models import SupportStaff, ServiceRequestNote

def create_superuser():
    if not User.objects.filter(username='admin').exists():
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        print(f"Superuser created: {superuser.username}")
    else:
        print("Superuser already exists")

def create_request_types():
    request_types = [
        {
            'name': 'Gas Leak',
            'description': 'Report a potential gas leak or gas smell in your area.'
        },
        {
            'name': 'Service Connection',
            'description': 'Request a new gas service connection for your property.'
        },
        {
            'name': 'Billing Issue',
            'description': 'Questions or problems regarding your gas bill.'
        },
        {
            'name': 'Meter Reading',
            'description': 'Request a meter reading or report a problem with your gas meter.'
        },
        {
            'name': 'Service Interruption',
            'description': 'Report a gas service interruption or outage.'
        },
        {
            'name': 'General Inquiry',
            'description': 'General questions about your gas service.'
        },
    ]
    
    for rt in request_types:
        ServiceRequestType.objects.get_or_create(
            name=rt['name'],
            defaults={'description': rt['description']}
        )
    
    print(f"Created {len(request_types)} service request types")

def create_customers():
    # Create test customers
    customer_data = [
        {
            'username': 'customer1',
            'email': 'customer1@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Main St, Anytown, USA',
            'phone': '555-123-4567'
        },
        {
            'username': 'customer2',
            'email': 'customer2@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'address': '456 Oak Ave, Somewhere, USA',
            'phone': '555-987-6543'
        }
    ]
    
    customers = []
    for data in customer_data:
        if not User.objects.filter(username=data['username']).exists():
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password='password123',
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            
            customer = Customer.objects.create(
                user=user,
                address=data['address'],
                phone_number=data['phone'],
                account_number=f"GAS{user.id:06d}"
            )
            customers.append(customer)
            print(f"Created customer: {customer.user.username}")
        else:
            print(f"Customer {data['username']} already exists")
    
    return customers

def create_support_staff():
    # Create test support staff
    staff_data = [
        {
            'username': 'support1',
            'email': 'support1@example.com',
            'first_name': 'Bob',
            'last_name': 'Johnson',
            'staff_id': 'ST001',
            'department': 'Customer Support'
        },
        {
            'username': 'support2',
            'email': 'support2@example.com',
            'first_name': 'Sarah',
            'last_name': 'Williams',
            'staff_id': 'ST002',
            'department': 'Technical Support'
        }
    ]
    
    staff_members = []
    for data in staff_data:
        if not User.objects.filter(username=data['username']).exists():
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password='password123',
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            
            staff = SupportStaff.objects.create(
                user=user,
                staff_id=data['staff_id'],
                department=data['department']
            )
            staff_members.append(staff)
            print(f"Created support staff: {staff.user.username}")
        else:
            print(f"Support staff {data['username']} already exists")
    
    return staff_members

def create_service_requests(customers, staff):
    # Get all request types
    request_types = list(ServiceRequestType.objects.all())
    if not request_types:
        print("No request types found. Cannot create service requests.")
        return
    
    # Create sample service requests
    sample_requests = [
        {
            'title': 'Gas smell in my basement',
            'description': 'I can smell gas in my basement. It started yesterday evening.',
            'status': 'IN_PROGRESS',
        },
        {
            'title': 'Need new gas connection',
            'description': 'I just bought a new house and need gas service connected.',
            'status': 'PENDING',
        },
        {
            'title': 'My bill seems too high',
            'description': 'My gas bill for this month is double what it normally is, but my usage hasn\'t changed.',
            'status': 'COMPLETED',
        },
        {
            'title': 'Meter not working correctly',
            'description': 'I think my gas meter might be broken. The display is showing strange numbers.',
            'status': 'PENDING',
        }
    ]
    
    now = timezone.now()
    
    for i, req_data in enumerate(sample_requests):
        # Alternate between customers
        customer = customers[i % len(customers)] if customers else None
        if not customer:
            continue
        
        request = ServiceRequest.objects.create(
            customer=customer,
            request_type=random.choice(request_types),
            title=req_data['title'],
            description=req_data['description'],
            status=req_data['status'],
            created_at=now - timedelta(days=random.randint(1, 30)),
        )
        
        # Assign to staff and add notes for some requests
        if req_data['status'] in ['IN_PROGRESS', 'COMPLETED']:
            request.assigned_to = random.choice(staff) if staff else None
            
            if request.assigned_to:
                ServiceRequestNote.objects.create(
                    service_request=request,
                    staff=request.assigned_to,
                    content=f"I'm looking into this issue and will update you soon.",
                    internal_only=False
                )
                
                ServiceRequestNote.objects.create(
                    service_request=request,
                    staff=request.assigned_to,
                    content=f"Customer called again about this issue today.",
                    internal_only=True
                )
            
        # Set resolved date for completed requests
        if req_data['status'] == 'COMPLETED':
            request.resolved_at = request.created_at + timedelta(days=random.randint(1, 5))
            
        request.save()
        print(f"Created service request: {request.title}")

def main():
    print("Setting up initial data for Gas Utility Service Application...")
    
    create_superuser()
    create_request_types()
    customers = create_customers()
    staff = create_support_staff()
    create_service_requests(customers, staff)
    
    print("Setup complete!")

if __name__ == "__main__":
    main()
