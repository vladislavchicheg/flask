def register_views():
    from blog import models
    from blog.extension import admin, db
    from blog.views.admin import ArticleAdminView, TagAdminView, UserAdminView

    admin.add_view(ArticleAdminView(models.Article, db.session, category="Models"))
    admin.add_view(TagAdminView(models.Tag, db.session, category="Models"))
    admin.add_view(UserAdminView(models.User, db.session, category="Models"))
