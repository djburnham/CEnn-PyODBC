--
-- Added view to make querying the normalised order structures easier
CREATE VIEW [v_customer_order_totals]
AS
SELECT c.customer_id, c.email, c.city, c.state
, ot.order_id, ot.order_date, ot.order_total_sale_price
FROM bs_customers AS c
JOIN (
			SELECT o.customer_id, o.order_id, o.order_date, od.order_total_sale_price
			FROM bs_orders AS o
			JOIN (
					SELECT order_id 
					,SUM((quantity * list_price) - (discount*quantity*list_price)) AS order_total_sale_price
					FROM bs_order_items
					GROUP BY order_id) AS od
			ON o.order_id = od.order_id ) AS ot
ON ot.customer_id = c.customer_id;