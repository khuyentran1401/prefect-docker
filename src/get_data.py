from pytrends.request import TrendReq
from prefect import flow, task
import plotly.express as px
import datapane as dp


@task(retries=3, retry_delay_seconds=10)
def get_pytrends(keyword: str):
    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload([keyword])
    return pytrends


@task
def get_interest_overtime(pytrends: TrendReq, keyword: str, start_date: str):
    df = pytrends.interest_over_time().loc[start_date:]
    fig = px.line(data_frame=df[keyword])
    return [dp.Text("# Interest Overtime"), dp.Plot(fig)]


@task
def get_interest_by_region(pytrends: TrendReq, keyword: str, num_countries: int):
    country = pytrends.interest_by_region(
        resolution="COUNTRY", inc_low_vol=True, inc_geo_code=False
    ).sort_values(by=keyword, ascending=False)
    fig = px.bar(data_frame=country[:num_countries])
    return [dp.Text("# Interest by Countries"), dp.Plot(fig)]


@task
def get_related_queries(pytrends: TrendReq, keyword: str):
    df = pytrends.related_queries()[keyword]["top"]
    fig = px.bar(data_frame=df, x="query", y="value")
    return [dp.Text(f"# Related Queries to {keyword}"), dp.Plot(fig)]


@flow(name="Get Google Trends for a Keyword")
def get_keywords_stats(keyword: str, start_date: str, num_countries: int):
    """Get statistics of a keyword on Google Trends"""
    pytrends = get_pytrends(keyword)
    interest_over_time = get_interest_overtime(pytrends, keyword, start_date)
    interest_by_region = get_interest_by_region(pytrends, keyword, num_countries)
    related_queries = get_related_queries(pytrends, keyword)
    return [*interest_over_time, *interest_by_region, *related_queries]


if __name__ == "__main__":
    keyword = "COVID"
    start_date = "2020-01-01"
    num_countries = 10
    get_keywords_stats(keyword, start_date, num_countries)
