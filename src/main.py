from get_data import get_keywords_stats
from create_report import create_report
from prefect import flow, task


@flow
def create_pytrends_report(keyword: str, start_date: str, num_countries: int):
    report_components = get_keywords_stats(keyword, start_date, num_countries)
    create_report(report_components, keyword)


if __name__ == "__main__":
    keyword = "COVID"
    start_date = '2020-01-01'
    num_countries = 10
    create_pytrends_report(keyword, start_date, num_countries)
