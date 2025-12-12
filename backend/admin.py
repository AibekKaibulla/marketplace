"""
Admin Panel Configuration using SQLAdmin
Access at: http://localhost:8000/admin
"""
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
import models
from auth_utils import verify_password, get_user_by_username
from database import SessionLocal


from logger import logger

class AdminAuth(AuthenticationBackend):
    """Authentication backend for admin panel"""
    
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        
        logger.info(f"Admin login attempt for user: {username}")
        
        # Verify credentials
        db = SessionLocal()
        try:
            user = get_user_by_username(db, username)
            if user:
                is_admin = user.role == "admin"
                is_valid_pw = verify_password(password, user.password_hash)
                
                if is_admin and is_valid_pw:
                    # Store admin session
                    request.session.update({"admin_user": username})
                    logger.info(f"Admin login successful for user: {username}")
                    return True
                else:
                    logger.warning(f"Admin login failed - Invalid role or password for user: {username}")
            else:
                logger.warning(f"Admin login failed - User not found: {username}")
        except Exception as e:
            logger.error(f"Admin login error: {e}")
        finally:
            db.close()
        
        return False
    
    async def logout(self, request: Request) -> bool:
        request.session.clear()
        logger.info("Admin logout")
        return True
    
    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("admin_user")
        if not token:
            return False
        return True


# ============== Model Views ==============

class UserAdmin(ModelView, model=models.User):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    
    column_list = [
        models.User.user_id,
        models.User.username,
        models.User.email,
        models.User.display_name,
        models.User.role,
        models.User.created_at
    ]
    
    column_searchable_list = [models.User.username, models.User.email, models.User.display_name]
    column_sortable_list = [models.User.user_id, models.User.username, models.User.created_at]
    column_default_sort = [(models.User.created_at, True)]
    
    form_excluded_columns = [models.User.password_hash, models.User.listings, models.User.favorites]
    
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class CategoryAdmin(ModelView, model=models.Category):
    name = "Category"
    name_plural = "Categories"
    icon = "fa-solid fa-folder"
    
    column_list = [
        models.Category.category_id,
        models.Category.name,
        models.Category.icon,
        models.Category.description
    ]
    
    column_searchable_list = [models.Category.name]
    
    can_create = True
    can_edit = True
    can_delete = True


class ListingAdmin(ModelView, model=models.Listing):
    name = "Listing"
    name_plural = "Listings"
    icon = "fa-solid fa-box"
    
    column_list = [
        models.Listing.listing_id,
        models.Listing.title,
        models.Listing.price,
        models.Listing.status,
        models.Listing.condition,
        models.Listing.view_count,
        models.Listing.created_at
    ]
    
    column_searchable_list = [models.Listing.title, models.Listing.description]
    column_sortable_list = [
        models.Listing.listing_id, 
        models.Listing.price, 
        models.Listing.created_at,
        models.Listing.view_count
    ]
    column_default_sort = [(models.Listing.created_at, True)]
    
    form_excluded_columns = [models.Listing.favorites, models.Listing.messages, models.Listing.photos]
    
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class MessageAdmin(ModelView, model=models.Message):
    name = "Message"
    name_plural = "Messages"
    icon = "fa-solid fa-envelope"
    
    column_list = [
        models.Message.message_id,
        models.Message.sender_id,
        models.Message.receiver_id,
        models.Message.body,
        models.Message.is_read,
        models.Message.sent_at
    ]
    
    column_sortable_list = [models.Message.message_id, models.Message.sent_at]
    column_default_sort = [(models.Message.sent_at, True)]
    
    can_create = False
    can_edit = True
    can_delete = True


class FavoriteAdmin(ModelView, model=models.Favorite):
    name = "Favorite"
    name_plural = "Favorites"
    icon = "fa-solid fa-heart"
    
    column_list = [
        models.Favorite.favorite_id,
        models.Favorite.user_id,
        models.Favorite.listing_id,
        models.Favorite.created_at
    ]
    
    can_create = False
    can_edit = False
    can_delete = True


class PhotoAdmin(ModelView, model=models.Photo):
    name = "Photo"
    name_plural = "Photos"
    icon = "fa-solid fa-image"
    
    column_list = [
        models.Photo.photo_id,
        models.Photo.listing_id,
        models.Photo.url,
        models.Photo.alt_text,
        models.Photo.sort_order
    ]
    
    can_create = True
    can_edit = True
    can_delete = True


def setup_admin(app, engine):
    """Setup admin panel and register all model views"""
    authentication_backend = AdminAuth(secret_key="super-secret-admin-key-change-in-production")
    
    admin = Admin(
        app, 
        engine,
        authentication_backend=authentication_backend,
        title="Student Marketplace Admin",
        base_url="/admin"
    )
    
    # Register model views
    admin.add_view(UserAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(ListingAdmin)
    admin.add_view(MessageAdmin)
    admin.add_view(FavoriteAdmin)
    admin.add_view(PhotoAdmin)
    
    return admin
