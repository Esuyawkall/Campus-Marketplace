
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

## 📦 Products (`product.py`)

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
- **Update**
  - (Optional) Edit messages
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
- **Read**
  - view Images
- **Create**
  - upload Images 

### Admin
- **Update**
  - Modify Images
- **Delete**
  - Remove Images

---

## Orders (`order.py`)

### Participant
- **Read**
  - see current and previous orders


### Admin
- **Read**
  - see and manage all user orders
- **Update**
  - Modify orders
- **Delete**
  - Remove orders

---

## 🚩 Reports / Flags (future moderation system)

### Participant
- **Create**
  - Report users or listings

### Admin
- **Read**
  - View reports
- **Update**
  - Mark as resolved
- **Delete**
  - Remove reports
