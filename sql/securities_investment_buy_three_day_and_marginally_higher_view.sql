CREATE OR REPLACE VIEW public.securities_investment_buy_three_day_and_marginally_higher_view
 AS
select a.*,c.stock_name from(
SELECT stock_id,sum(securities_investment_difference) as total
FROM public.twse_institutional_investors
where stock_date in (select stock_date from twse_institutional_investors where stock_id='2330' order by stock_date desc limit 3)
AND securities_investment_difference>0 group by stock_id having count(stock_id)=3
) as a
inner join (
SELECT stock_id
	FROM public.stock_base_data
	where stock_date in (select stock_date from twse_institutional_investors where stock_id='2330' order by stock_date desc limit 3)
	GROUP BY stock_id
	having max(closing_price)/min(closing_price)<1.03
) as b
on a.stock_id = b.stock_id
left join (
	SELECT stock_id,stock_name
		FROM public.stocks group by stock_id,stock_name
) as c
on a.stock_id = c.stock_id
;

ALTER TABLE public.securities_investment_buy_three_day_and_marginally_higher_view
    OWNER TO postgres;