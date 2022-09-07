from get_data import get_keywords_stats
from create_report import create_report
from prefect import flow


@flow(name="Create a Report for Google Trends")
def create_pytrends_report(
    keyword: str = "COVID", start_date: str = "2020-01-01", num_countries: int = 10
):
    report_components = get_keywords_stats(keyword, start_date, num_countries)
    create_report(report_components, keyword)


if __name__ == "__main__":
    create_pytrends_report()
