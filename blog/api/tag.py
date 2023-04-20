from flask_combo_jsonapi import ResourceDetail, ResourceList

from blog.extension import db
from blog.models import Tag
from blog.schemas import TagSchema


class TagList(ResourceList):
    schema = TagSchema
    data_layer = {
        "session": db.session,
        "model": Tag,
    }


class TagDetail(ResourceDetail):
    schema = TagSchema
    data_layer = {
        "session": db.session,
        "model": Tag,
    }
