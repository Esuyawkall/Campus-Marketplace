
---

# User Roles

## 1. Admin
- Full control over platform data and moderation

## 2. Participant
- Regular user (buyer + seller)

---

# CRUD OPERATIONS

## Users (`user.py`)

### Participant
- **Create**
  - Register account
- **Read**
  - View own profile
  - View other users (seller info)
- **Update**
  - Edit profile (name, email, password)
- **Delete**
  - Delete own account

### Admin
- **Create**
  - Add users manually (optional)
- **Read**
  - View all users
  - Search/filter users
- **Update**
  - Change roles (`admin`, `participant`)
  - Update status (`active`, `suspended`, `banned`)
- **Delete**
  - Remove users

---

## Products (`product.py`)

### Participant (Seller)
- **Create**
  - Add new listing
- **Read**
  - View all listings
  - View own listings
- **Update**
  - Edit own listings
- **Delete**
  - Delete own listings

### Admin
- **Read**
  - View all products
- **Update**
  - Edit any listing
- **Delete**
  - Remove inappropriate listings

---

## Messaging (`message.py`)

### Participant
- **Create**
  - Send messages
- **Read**
  - View conversations
- **Delete**
  - Delete messages

### Admin
- **Read**
  - Monitor conversations
- **Delete**
  - Remove harmful content

---

## Images (`image.py`)

### Participant
- **Create**
  - Upload images
- **Read**
  - View images
- **Update**
  - Modify own images
- **Delete**
  - Delete own images

### Admin
- **Read**
  - View all images
- **Update**
  - Modify any images
- **Delete**
  - Remove inappropriate images

---

## Orders (`order.py`)

### Participant
- **Create**
  - Place orders
- **Read**
  - View current and previous orders
- **Update**
  - Modify order status/details
- **Delete**
  - Cancel orders

### Admin
- **Read**
  - View and manage all user orders
- **Update**
  - Modify any order
- **Delete**
  - Remove orders

---

## Favorites (`favorite.py`)

### Participant
- **Create**
  - Add products to favorites
- **Read**
  - View favorite products
- **Delete**
  - Remove products from favorites

### Admin
- **Read**
  - View all favorites (optional)
