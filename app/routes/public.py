import json
from datetime import datetime

from flask import Blueprint, render_template, abort, url_for, Response

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
    json_ld = {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "headline": resource['title'],
        "datePublished": resource['publishTime'],
        "author": {
            "@type": "Person",
            "name": resource['createdBy']['name']
        },
        "url": url_for('public.resource_detail', slug=resource['slug'], _external=True),
    }
    if not resource:
        abort(404)
    return render_template("views/resource_detail.html", resource=resource, json_ld_data=json.dumps(json_ld))

@public_bp.route("/about")
def about():
    masthead_cta = True
    return render_template("views/about.html", **locals())

@public_bp.route("/contact")
def contact():
    masthead_cta = True
    return render_template("views/contact.html", **locals())


@public_bp.route('/sitemap.xml', methods=['GET'])
def sitemap():
    pages = []
    lastmod = datetime.now().date().isoformat()

    # Static pages
    static_pages = [
        {'endpoint': 'public.home', 'changefreq': 'monthly', 'priority': 0.9},
        {'endpoint': 'public.services', 'changefreq': 'monthly', 'priority': 1.0},
        {'endpoint': 'public.contact', 'changefreq': 'monthly', 'priority': 0.3},
        {'endpoint': 'public.about', 'changefreq': 'monthly', 'priority': 0.8},
        {'endpoint': 'public.resources', 'changefreq': 'monthly', 'priority': 0.9},
    ]

    for page in static_pages:
        url = url_for(page['endpoint'], _external=True)
        pages.append(f"""
        <url>
            <loc>{url}</loc>
            <lastmod>{lastmod}</lastmod>
            <changefreq>{page['changefreq']}</changefreq>
            <priority>{page['priority']}</priority>
        </url>
        """)

    # Dynamic resource pages
    resources = fetch_resources()
    for resource in resources:
        url = url_for('public.resource_detail', slug=resource['slug'], _external=True)
        pages.append(f"""
        <url>
            <loc>{url}</loc>
            <lastmod>{lastmod}</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.7</priority>
        </url>
        """)

    # Compile full XML
    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        {''.join(pages)}
    </urlset>"""

    return Response(sitemap_xml, mimetype='application/xml')