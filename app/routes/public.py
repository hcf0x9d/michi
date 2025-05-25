from flask import Blueprint, render_template, abort

from app.services.hygraph import fetch_resources, fetch_resource_by_slug

public_bp = Blueprint("public", __name__)

@public_bp.route("/")
def home():
    masthead_cta = True
    return render_template("views/home.html", **locals())

@public_bp.route("/services")
def services():
    masthead_cta = True
    return render_template("views/services.html", **locals())

@public_bp.route("/resources")
def resources():
    resource_list = fetch_resources()
    return render_template("views/resources.html", **locals())


@public_bp.route("/resources/<slug>")
def resource_detail(slug):
    resource = fetch_resource_by_slug(slug)
    if not resource:
        abort(404)
    return render_template("views/resource_detail.html", resource=resource)

@public_bp.route("/about")
def about():
    masthead_cta = True
    return render_template("views/about.html", **locals())

@public_bp.route("/contact")
def contact():
    masthead_cta = True
    return render_template("views/contact.html", **locals())
