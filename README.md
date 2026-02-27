# Snacks Billing & Business Management System

A complete, professional billing and business management web application designed for snacks manufacturing and selling businesses. Built with Django, featuring GST-compliant invoicing, inventory management, customer tracking, expense management, and comprehensive business analytics.

## Features

- **Authentication & Security**
  - Google OAuth 2.0 integration
  - Django Admin authentication
  - Secure session management
  - CSRF protection

- **Dashboard**
  - Real-time business summary cards
  - Sales, expenses, and profit tracking
  - Monthly performance metrics
  - Quick action buttons
  - Recent invoice history

- **Product Management**
  - Add, edit, and delete products
  - Product images and categorization
  - MRP and retail pricing
  - GST rate management
  - Manufacture date tracking

- **Billing System**
  - GST-compliant invoice generation
  - Auto-generated invoice numbers
  - Invoice items with line totals
  - Automatic GST calculations
  - Invoice status tracking (Draft, Sent, Paid, Cancelled)
  - PDF invoice generation

- **Customer Management**
  - Create and manage customer profiles
  - Retail and wholesale customer types
  - Customer balance tracking
  - Transaction history
  - GST number management

- **Expense & Payment Tracking**
  - Expense categorization (Raw Material, Rent, Utilities, etc.)
  - Payment recording from customers
  - Multiple payment methods
  - Customer balance auto-updates
  - Financial summary reports

- **Labour Management**
  - Worker registration
  - Daily attendance tracking
  - Automated wage calculation
  - Monthly wage summaries
  - Payment records

- **Reports & Analytics**
  - Profit & Loss statements
  - Sales analysis
  - Expense breakdowns
  - Labour cost reports
  - Customizable date ranges
  - Charts and visualizations

## Technology Stack

- **Backend**: Python 3, Django 4.2
- **Database**: SQLite (production-ready for small businesses)
- **Frontend**: HTML5, Vanilla JavaScript
- **Styling**: Tailwind CSS
- **Authentication**: Django Allauth (OAuth 2.0 + Traditional)
- **Additional**: Pillow (Image handling)

## Project Structure

```
project_root/
├── manage.py                 # Django management script
├── db.sqlite3               # Database file
│
├── config/                  # Django configuration
│   ├── settings.py         # Project settings
│   ├── urls.py             # URL routing
│   ├── wsgi.py             # WSGI configuration
│   └── __init__.py
│
├── apps/
│   ├── core/               # Core functionality
│   │   ├── models.py       # BusinessProfile model
│   │   ├── views.py        # Dashboard view
│   │   ├── urls.py         # Core URLs
│   │   └── admin.py        # Admin configuration
│   │
│   ├── products/           # Product management
│   │   ├── models.py       # Product model
│   │   ├── views.py        # CRUD operations
│   │   ├── urls.py         # Product URLs
│   │   └── admin.py        # Admin panel
│   │
│   ├── billing/            # Invoicing system
│   │   ├── models.py       # Invoice & InvoiceItem models
│   │   ├── views.py        # Invoice operations
│   │   ├── urls.py         # Billing URLs
│   │   └── admin.py        # Admin configuration
│   │
│   ├── customers/          # Customer management
│   │   ├── models.py       # Customer model
│   │   ├── views.py        # Customer operations
│   │   ├── urls.py         # Customer URLs
│   │   └── admin.py        # Admin panel
│   │
│   ├── expenses/           # Expense & payment tracking
│   │   ├── models.py       # Expense & Payment models
│   │   ├── views.py        # Expense operations
│   │   ├── urls.py         # Expense URLs
│   │   └── admin.py        # Admin configuration
│   │
│   ├── labour/             # Labour management
│   │   ├── models.py       # Labour, Attendance, Wage models
│   │   ├── views.py        # Labour operations
│   │   ├── urls.py         # Labour URLs
│   │   └── admin.py        # Admin panel
│   │
│   └── reports/            # Business reports
│       ├── views.py        # Report generation
│       └── urls.py         # Report URLs
│
├── templates/              # HTML templates
│   ├── base.html          # Master layout
│   ├── login.html         # Google login page
│   ├── dashboard.html     # Main dashboard
│   │
│   ├── components/
│   │   ├── navbar.html    # Top navigation
│   │   └── sidebar.html   # Side navigation
│   │
│   ├── products/
│   │   ├── product_list.html
│   │   └── product_form.html
│   │
│   ├── billing/
│   │   ├── invoice_list.html
│   │   ├── invoice_form.html
│   │   └── invoice_detail.html
│   │
│   ├── customers/
│   │   ├── customer_list.html
│   │   ├── customer_form.html
│   │   └── customer_detail.html
│   │
│   ├── expenses/
│   │   ├── expense_list.html
│   │   ├── payment_list.html
│   │   └── forms
│   │
│   ├── labour/
│   │   ├── labour_list.html
│   │   ├── labour_detail.html
│   │   └── wage_summary.html
│   │
│   └── reports/
│       ├── dashboard.html
│       ├── profit_loss.html
│       └── sales.html
│
├── static/                 # Static files
│   ├── css/
│   │   └── main.css       # Tailwind & custom styles
│   │
│   └── js/
│       └── main.js        # Client-side functionality
│
├── media/                  # User uploaded files
│   └── uploads/
│
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment support

### Step 1: Clone or Download the Project

```bash
git clone <repository-url>
cd snacks-billing
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Apply Database Migrations

```bash
python manage.py migrate
```

### Step 5: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### Step 6: Setup Google OAuth (Optional but Recommended)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials (Web application)
5. Add your redirect URI: `http://localhost:8000/accounts/google/callback/`
6. Copy Client ID and Client Secret
7. Log in to Django Admin: `http://localhost:8000/admin/`
8. Go to Sites and add your domain
9. Go to Social Applications
10. Add Google with your Client ID and Secret

### Step 7: Run Development Server

```bash
python manage.py runserver
```

Access the application at `http://localhost:8000/`

### Default URLs

- **Main Dashboard**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **Products**: http://localhost:8000/products/
- **Billing**: http://localhost:8000/billing/
- **Customers**: http://localhost:8000/customers/
- **Expenses**: http://localhost:8000/expenses/
- **Labour**: http://localhost:8000/labour/
- **Reports**: http://localhost:8000/reports/

## Database Models

### Core App
- **BusinessProfile**: Store business information

### Products App
- **Product**: Snack products with pricing and GST info

### Billing App
- **Invoice**: GST-compliant invoices
- **InvoiceItem**: Individual items in an invoice

### Customers App
- **Customer**: Customer profiles with balance tracking

### Expenses App
- **Expense**: Business expenses
- **Payment**: Customer payments received

### Labour App
- **Labour**: Worker records
- **Attendance**: Daily attendance tracking
- **Wage**: Wage payment records

### Reports App
- Analytics and reporting views

## API Endpoints

All endpoints require authentication. Format: JSON for AJAX requests.

### Products
- `GET /products/` - List products
- `POST /products/create/` - Create product
- `POST /products/<id>/edit/` - Edit product
- `POST /products/<id>/delete/` - Delete product

### Billing
- `GET /billing/` - List invoices
- `POST /billing/create/` - Create invoice
- `GET /billing/<id>/` - View invoice
- `POST /billing/<id>/status/` - Update invoice status
- `GET /billing/<id>/pdf/` - Download invoice PDF

### Customers
- `GET /customers/` - List customers
- `POST /customers/create/` - Create customer
- `GET /customers/<id>/` - View customer details
- `POST /customers/<id>/edit/` - Edit customer
- `POST /customers/<id>/delete/` - Delete customer

### Expenses
- `GET /expenses/` - List expenses
- `POST /expenses/create/` - Create expense
- `POST /expenses/<id>/delete/` - Delete expense
- `GET /expenses/payments/` - List payments
- `POST /expenses/payments/create/` - Record payment

### Labour
- `GET /labour/` - List workers
- `POST /labour/create/` - Add worker
- `GET /labour/<id>/` - View worker details
- `POST /labour/<id>/attendance/` - Mark attendance
- `GET /labour/wages/` - View wage summary

### Reports
- `GET /reports/` - Dashboard reports
- `GET /reports/profit-loss/` - P&L report
- `GET /reports/sales/` - Sales analysis
- `GET /reports/labour/` - Labour cost report

## Security Features

- ✅ CSRF protection on all forms
- ✅ SQL Injection prevention (ORM)
- ✅ Secure password hashing
- ✅ User authentication required
- ✅ Admin-only access to configuration
- ✅ OAuth 2.0 secure authentication
- ✅ Session management
- ✅ XSS protection

## Browser Compatibility

- Chrome (Latest)
- Firefox (Latest)
- Safari (Latest)
- Edge (Latest)

## Troubleshooting

### Module not found errors
```bash
pip install -r requirements.txt
```

### Database errors
```bash
python manage.py migrate
```

### Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Port 8000 already in use
```bash
python manage.py runserver 8080
```

## Best Practices

1. **Backup your database regularly**
   ```bash
   python manage.py dumpdata > backup.json
   ```

2. **Update dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Use strong admin passwords**

4. **Enable HTTPS in production**

5. **Set DEBUG = False in production**

## Performance Tips

- Use pagination for large datasets
- Cache frequently accessed data
- Optimize database queries
- Compress static files
- Use CDN for media files

## Future Enhancements

- [ ] Multi-user support with role-based access
- [ ] Inventory management
- [ ] Automated email notifications
- [ ] WhatsApp integration
- [ ] Mobile app
- [ ] Cloud backup
- [ ] Advanced tax calculations
- [ ] Credit/debit note management
- [ ] Purchase order system
- [ ] Stock tracking

## License

This project is provided as-is for commercial use.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Django documentation
3. Check application logs
4. Contact administrator

## Credits

Built with:
- Django Framework
- Tailwind CSS
- Chart.js
- Django-allauth

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Production Ready
