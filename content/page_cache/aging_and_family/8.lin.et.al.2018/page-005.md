---
course: "aging_and_family"
source_pdf: "8.Lin.et.al.2018.pdf"
pdf_page: 5
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/aging_and_family/8.Lin.et.al.2018.pdf"
generated_at: "2026-09-01T06:26:38Z"
---
1026                                                               Journals of Gerontology: SOCIAL SCIENCES, 2018, Vol. 73, No. 6


Marital quality                                                two dimensions of the marital biography with the expecta-
Marital interaction was captured for wives and husbands.       tion that marriage order was less consequential at higher
It was constructed from two questions that indicate the        marital durations. Then we calculated bivariate statistics to
wife’s and the husband’s reports of how they allocated their   show how the means or percentages of each variable dif-
free time together (1 = mostly together, 2 = some together,    fered for the couples who experienced a gray divorce and
some apart, 3 = mostly apart) and how much they enjoyed        those who remained married (or were censored). Finally,
the time spent together (1 = extremely enjoyable, 2 = very     we conducted the multivariate analyses, which involved
enjoyable, 3 = somewhat enjoyable, 4 = not too enjoyable).     estimating discrete-time event history models predicting
Because few respondents reported time together as not too      gray divorce using logistic regression.
enjoyable, we combined this response category with some-           Event-history modeling is the most effective approach
what enjoyable, similar to Bulanda’s study (Bulanda, 2011).    to handle the problems posed by censoring (e.g., persons
Answers to these two questions were summed and reverse         continue to be at risk for an event after the observation
coded so that higher values represent more positive mari-      period ends) as well as time-varying explanatory variables
tal interaction, ranging from 2 to 6. Since these questions    that are integral to process-driven events such as divorce
were asked only the first time couples were interviewed,       (Allison, 1982). Discrete-time (vs. continuous-time) mod-
the wife’s and husband’s reports of marital quality were       els are appropriate here because the start and end dates of
treated as time-invariant covariates. Note that for couples    marriage were measured using time intervals. Discrete-time
who were first interviewed in 1992 and remained married        models have many advantages, including the ease of incor-
in 1998, their marital quality scores were obtained from       porating time-varying covariates and the use of log linear
the 1992 interview. For couples who were first interviewed     methods for model estimation. The model is specified as
in 1992, broke up, and remarried to other persons by 1998,     follows:
their marital quality scores were obtained from the inter-                     Pit = 1 / [1 + exp (−α t − β ’ xit )]
view when they first reported being remarried.                  Pit is the hazard rate, defined by Pit = Pr(T = t,| T ≥ t),
                                                               where T is the discrete random variable giving the uncen-
Spousal homogamy                                               sored time of event occurrence (Allison, 1982). In other
Husband’s age was measured in years and treated as a           words, Pit is the conditional probability that divorce
time-varying covariate. The couple’s age homogamy was          occurs to couple i at time t, given that it has not already
defined as the difference between the husband’s and the        occurred. We consider how this hazard rate is a function of
wife’s ages and thus was time invariant. Racial homogamy,      time (α t ) and a vector of explanatory variables (xit , with
a time-invariant covariate, was captured by whether both       its coefficient vector β). Couples were observed from the
spouses were White (reference category), both spouses were     earliest time point at which they were (a) married and (b) at
non-White (1 = Yes, 0 = No), or spouses belonged to differ-    least one spouse was aged 50 or older. All couples entered
ent racial backgrounds (1 = Yes, 0 = No). Husband’s edu-       the analysis beginning with the first interview at which they
cational attainment was gauged by a continuous measure         were married (1998 or later). They were censored once
indicating the total number of years of schooling completed    they divorced, when one of the spouses died, or at the 2012
and ranged from 0 to 17. Education homogamy was cap-           interview (or attrition).
tured by taking the difference between the husband’s and           The initial model introduced the three later life tran-
the wife’s years of schooling. The education measures were     sition indicators: empty nest, wife’s retirement and hus-
time invariant.                                                band’s retirement, and wife’s chronic conditions and
                                                               husband’s chronic conditions. The second model added
Shared economic resources                                      all of the sociodemographic controls to assess the extent
Home ownership was a time-varying covariate indicating         to which the role of transitions was accounted for by the
whether the couple owned their home at a given interview-      more traditional predictors of divorce. Additional analy-
year (1 = Yes, 0 = No). The couple’s assets, also time-var-    ses were conducted to examine potential interaction effects
ying covariates, were composed of six categories: in debt,     for the later life transitions with marital biography and
$0 to $50,000 (reference category), $50,001 to $100,000,       marital quality. All models included interview year dummy
$100,001 to $250,000, and $250,001 or more. Both sets of       variables to account for the effect of time. Gray divorce
variables were lagged by one interview-wave (i.e., 2 years)    is more common today than two decades ago (Brown &
to establish the temporal order prior to divorce.              Lin, 2012). Missing data were minimal. On the core inde-
                                                               pendent measures of life transitions, for example, just
                                                               1%–3% of cases were missing. A multiple imputation pro-
Analytic Strategy                                              cedure, Multivariate Imputation using Chained Equations
We began by estimating the survival probabilities for cou-     (MICE), was performed using Stata’s mi impute chained
ples by marital duration. Estimates were conducted sepa-       command to handle missing cases such that the missing
rately for couples in first marriages versus remarriages to    value for a single variable was imputed as a function of
assess the potential for an interaction effect between these   other covariates in the analysis (Raghunathan, Lepkowski,
