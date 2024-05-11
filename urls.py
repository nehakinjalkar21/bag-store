from main import app
import category_op as ct
import bag as bg
import admin as ad
import users as us

# Category urls
app.add_url_rule("/showAllCategories",view_func=ct.showAllCategories)
app.add_url_rule("/addCategory",view_func=ct.addNewCategory,methods=["GET","POST"])
app.add_url_rule("/delete_cat/<cid>",view_func=ct.deleteCategory,methods=["GET","POST"])
app.add_url_rule("/edit_cat/<cid>",view_func=ct.editCategory,methods=["GET","POST"])

# Bag urls
app.add_url_rule("/showAllBags",view_func=bg.showAllBags)
app.add_url_rule("/addBag",view_func=bg.addNewBag,methods=["GET","POST"])
app.add_url_rule("/delete_bag/<bagid>",view_func=bg.deleteBags,methods=["GET","POST"])
app.add_url_rule("/edit_bag/<bagid>",view_func=bg.editBags,methods=["GET","POST"])

# Admin urls
app.add_url_rule("/adminLogin",view_func=ad.adminlogin,methods=["GET","POST"])
app.add_url_rule("/AdminPage",view_func=ad.adminPage)
app.add_url_rule("/AdminLogout",view_func=ad.adminLogout)

# Usersite urls
app.add_url_rule("/",view_func=us.homePage)
app.add_url_rule("/showBags/<cid>",view_func=us.showBags)
app.add_url_rule("/viewDetails/<bagid>",view_func=us.viewDetails)
app.add_url_rule("/login",view_func=us.login,methods=["GET","POST"])
app.add_url_rule("/signup",view_func=us.signup,methods=["GET","POST"])
app.add_url_rule("/logout",view_func=us.logout,methods=["GET","POST"])
app.add_url_rule("/addToCart",view_func=us.addToCart,methods=["POST"])
app.add_url_rule("/showCart",view_func=us.showCart,methods=["GET","POST"])
app.add_url_rule("/makePayment",view_func=us.makePayment,methods=["GET","POST"])
app.add_url_rule("/Wishlist/<bagid>",view_func=us.Wishlist)
app.add_url_rule("/addToWishlist",view_func=us.addToWishlist,methods=["POST"])
app.add_url_rule("/showWishlist",view_func=us.showWishlist,methods=["GET","POST"])
app.add_url_rule("/search",view_func=us.search,methods=["POST"])
app.add_url_rule("/",view_func=us.sendConfirmationEmail)










