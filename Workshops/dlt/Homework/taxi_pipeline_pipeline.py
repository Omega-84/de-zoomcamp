"""A dlt pipeline to ingest NYC taxi data from a REST API."""

import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import BasePaginator
from dlt.sources.helpers.requests import Response


class StopOnEmptyPaginator(BasePaginator):
    """Page-number paginator that stops when an empty JSON array is returned."""

    def __init__(self, start_page: int = 1):
        super().__init__()
        self._page = start_page

    def init_request(self, request):
        request.params = request.params or {}
        request.params["page"] = self._page

    def update_state(self, response: Response, data=None) -> None:
        if not response.json():
            self._has_next_page = False
        else:
            self._page += 1
            self._has_next_page = True

    def update_request(self, request):
        request.params = request.params or {}
        request.params["page"] = self._page


@dlt.source
def taxi_api_source():
    """Define dlt resources from the NYC Taxi REST API."""
    client = RESTClient(
        base_url="https://us-central1-dlthub-analytics.cloudfunctions.net/",
        paginator=StopOnEmptyPaginator(start_page=1),
    )

    @dlt.resource(name="rides", write_disposition="replace")
    def rides_resource():
        for page in client.paginate("data_engineering_zoomcamp_api"):
            yield page

    yield rides_resource()


pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline",
    destination="duckdb",
    dataset_name="taxi_data",
)


if __name__ == "__main__":
    load_info = pipeline.run(taxi_api_source())
    print(load_info)  # noqa: T201
