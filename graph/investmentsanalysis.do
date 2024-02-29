*******************************************************************************************************
/* This do-file runs the regression for Table  A6*/
*******************************************************************************************************
use Output\data\stata\companyfundperformanceregs, clear  


*Success regs
eststo clear
eststo:  reghdfe success  minority_funds minority_funds2 ln_funding, absorb(vintage firstdeal) vce(cluster investorid) 
eststo:  reghdfe success interactionone interactiontwo minority_funds minority_funds2 is_minority_founder ln_funding, absorb(vintage firstdeal) vce(cluster investorid) 
eststo:  reghdfe success interactionone interactiontwo minority_funds minority_funds2 is_minority_founder ln_funding, absorb(vintage state_fips firstdeal) vce(cluster investorid)
eststo:  reghdfe success interactionone interactiontwo minority_funds minority_funds2 is_minority_founder ln_fundno ln_size venture ln_age ln_funding, absorb(vintage state_fips firstdeal) vce(cluster investorid) 
esttab _all using "Output/tables/portfolio_companyms.tex", replace /// 
		star(* 0.10 ** 0.05 *** 0.01) se(3) b(3) ///
		order(interactionone interactiontwo minority_funds minority_funds2  minority_investment) ///
		ar2  noomitted  interaction(" $\times$ ") style(tex) ///
		compress nomtitles fragment noconst label nocons





