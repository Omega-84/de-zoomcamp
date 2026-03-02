"""A dlt pipeline to ingest data from the Open Library Search API."""

import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig


@dlt.source
def open_library_rest_api_source():
    """Define dlt resources from the Open Library REST API endpoints."""
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://openlibrary.org",
            # Open Library Search API is public — no auth required
        },
        "resources": [
            {
                "name": "harry_potter_books",
                "endpoint": {
                    "path": "search.json",
                    "params": {
                        "q": "harry potter",
                        "limit": 50,
                    },
                    "data_selector": "docs",
                    "paginator": {
                        "type": "page_number",
                        "page_param": "page",
                        "total_path": "num_found",
                        "base_page": 1,
                        "maximum_page": 5,
                    },
                },
            },
        ],
    }

    yield from rest_api_resources(config)


pipeline = dlt.pipeline(
    pipeline_name="open_library_pipeline",
    destination="duckdb",
    dataset_name="open_library_data",
    refresh="drop_sources",
    progress="log",
)


if __name__ == "__main__":
    load_info = pipeline.run(open_library_rest_api_source())
    print(load_info)  # noqa: T201
