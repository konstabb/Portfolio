

aineisto <- readxl::read_excel("PATH/Fertility_Small.xls")

#a)
perusOLS <- lm(weeksm1 ~ morekids, data = aineisto)
hrob_kesk_virh <- sandwich::vcovHC(perusOLS, type="HC1")
lmtest::coeftest(perusOLS, vcov. = hrob_kesk_virh)
#           Estimate Std. Error t value  Pr(>|t|)
#(Intercept) 21.47820    0.16368 131.220 < 2.2e-16 ***
#morekids    -6.00822    0.25410 -23.645 < 2.2e-16 ***

#c)
ekavaihe <- lm(morekids ~ samesex, data = aineisto)
hrob_kesk_virh <- sandwich::vcovHC(ekavaihe, type="HC1")
lmtest::coeftest(ekavaihe, vcov. = hrob_kesk_virh)
#             Estimate Std. Error t value  Pr(>|t|)
#(Intercept) 0.3439785  0.0038911  88.401 < 2.2e-16 ***
#samesex     0.0668197  0.0055836  11.967 < 2.2e-16 ***

#e)
car::linearHypothesis(ekavaihe, hypothesis.matrix=c("samesex=0"), vcov.=hrob_kesk_virh)
#Linear hypothesis test:
#samesex = 0

#Model 1: restricted model
#Model 2: morekids ~ samesex

#Note: Coefficient covariance matrix supplied.

#  Res.Df Df      F    Pr(>F)
#1  29999
#2  29998  1 143.21 < 2.2e-16 ***


#f)
instrumentilla <- AER::ivreg(weeksm1 ~ morekids | samesex, data = aineisto)
hrob_kesk_virh <- sandwich::vcovHC(instrumentilla, type="HC1")
lmtest::coeftest(instrumentilla, vcov.=hrob_kesk_virh)
#           Estimate Std. Error t value Pr(>|t|)
#(Intercept)  21.4876     1.4253 15.0759   <2e-16 ***
#morekids     -6.0332     3.7583 -1.6053   0.1084

#g)
laajemmin <- AER::ivreg(weeksm1 ~ morekids + agem1 + black + hispan + othrace | samesex + agem1 + black + hispan + othrace, data = aineisto)
hrob_kesk_virh <- sandwich::vcovHC(laajemmin, type="HC1")
lmtest::coeftest(laajemmin, vcov.=hrob_kesk_virh)
#             Estimate Std. Error t value  Pr(>|t|)
#(Intercept) -4.370342   1.178046 -3.7098 0.0002078 ***
#morekids    -5.780746   3.644953 -1.5860 0.1127592
#agem1        0.823497   0.069271 11.8880 < 2.2e-16 ***
#black       11.426280   0.658269 17.3581 < 2.2e-16 ***
#hispan      -0.411768   0.749322 -0.5495 0.5826527
#othrace      3.307789   0.612599  5.3996  6.73e-08 ***


lmtest::coeftest(malli, vcov.=hrob_kesk_virh)
#            Estimate Std. Error t value  Pr(>|t|)
#(Intercept) 0.400000   0.049237  8.1240 4.774e-14 ***
#men         0.200000   0.069631  2.8723  0.004519 **
