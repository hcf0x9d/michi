import os
import requests
from config import HYGRAPH_API_URL


def fetch_resources():
    """Fetch all Resource entries from Hygraph"""
    query = """
    {
      resources(orderBy: publishTime_DESC) {
        title
        slug
        thumbnail {
          fileName
          url
        }
        resourceType
        gateUrl
        summary
        file {
          url
          mimeType
          fileName
        }
      }
    }
    """
    response = requests.post(HYGRAPH_API_URL, json={"query": query})
    print(response.json())
    if response.status_code == 200:
        return response.json().get("data", {}).get("resources", [])
    else:
        print(f"Error fetching services: {response.status_code} - {response.text}")
        return []

def fetch_resource_by_slug(slug):
    """Fetch a single resource entry by slug from Hygraph"""
    query = """
    query GetResourceBySlug($slug: String!) {
      resource(where: { slug: $slug }) {
        title
        slug
        resourceType
        pullQuote
        tag
        keyImage {
          fileName
          url
        }
        summary
        content
        createdBy {
          name
        }
        publishTime
        file {
          url
          mimeType
          fileName
        }
        ctaHeadline
        ctaBody
        ctaLabel
        ctaLink
      }
    }
    """
    variables = { "slug": slug }

    response = requests.post(
        HYGRAPH_API_URL,
        json={"query": query, "variables": variables}
    )

    if response.status_code == 200:
        return response.json().get("data", {}).get("resource")
    else:
        print(f"Error fetching resource by slug: {response.status_code} - {response.text}")
        return None