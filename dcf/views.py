from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse, HttpResponse

from .utils.data.get_statements import get_statement
from .utils.tools.fundamentals_class import Fundamentals 

import json 

# Create your views here.
# a view is essentially a request handler

def test(request):
    print('------------------------------------')
    print('request: ', request)
    if request.method=="POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        # print(body)
        ticker = body["ticker"]
        earningsGrowthRate = body["earningsGrowthRate"]
        earningsGrowthRate = body["earningsGrowthRate"]
        capExGrowthRate = body["capExGrowthRate"]
        perpetualGrowthRate = body["perpetualGrowthRate"]
        bound = body["bound"]
        # confidenceIntervals = body["confidenceIntervals"]
        # confidenceIntervalMax = body["confidenceIntervalMax"]
        api = '98c7e0304749128f76f1aabf30e3e165'

    inc = get_statement(company_ticker = ticker,
                    statement_name = 'income-statement',
                    api_key = api
                    )
    bs = get_statement(company_ticker = ticker,
                        statement_name = 'balance-sheet-statement',
                        api_key = api
                        )
    bsq = get_statement(company_ticker = ticker,
                        statement_name = 'balance-sheet-statement',
                        api_key = api,
                        frequency = 'quarter'
                        )
    cf = get_statement(company_ticker = ticker,
                        statement_name = 'cash-flow-statement',
                        api_key = api
                        )
    ev = get_statement(company_ticker = ticker,
                        statement_name = 'enterprise-value',
                        api_key = api
                        )
    fr = get_statement(company_ticker = ticker,
                        statement_name = 'financial-ratios',
                        api_key = api,
                        )
    
    #create the dcf object
    company = Fundamentals(income_statement = inc,
          balance_sheet_statement = bs,
          balance_sheet_statement_quarterly = bsq,
          cash_flow_statement = cf,
          enterprise_value = ev,
          financial_ratios = fr,
          company_ticker = ticker,
          forecasting_period = 4,
          api_key = api)

    company.get_interest_coverage_and_risk_free_rate()
    company.get_cost_of_debt()
    company.get_cost_of_equity()
    company.get_wacc()
    company.get_enterprise_value(earningsGrowthRate, capExGrowthRate, perpetualGrowthRate)
    company.get_equity_value()
    company.f_score()

    return JsonResponse({
            "params": {
                "ticker": ticker,
                "earningsGrowthRate": earningsGrowthRate,
                "capExGrowthRate": capExGrowthRate,
                "perpetualGrowthRate": perpetualGrowthRate,
                "bound": bound,
                # "confidenceIntervalMin": confidenceIntervalMin,
                # "confidenceIntervalMax": confidenceIntervalMax
            },
            "dcf": {
                "interestCoverageRatio": "%.2f" % company.interest_coverage_ratio,
                "riskFreeRate": "%.4f" % company.risk_free_rate,
                "costOfDebt": "%.4f" % company.cost_of_debt,
                "capm": "%.4f" % company.capm,
                "wacc": "%.4f" % company.wacc,
                "enterpriseValue": "%.2f" % company.enterprise_value,
                "equityValue": "%.2f" % company.equity_value,
                "sharePrice": "%.2f" % company.share_price
            },
            "fscore": company.fscore
        })

