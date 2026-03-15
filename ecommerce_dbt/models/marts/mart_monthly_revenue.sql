with orders as (
    select * from {{ref('int_orders_with_customers')}}
),

monthly as(
    select
        date_trunc('month', purchased_at)   as month,
        count(DISTINCT order_id)    as total_orders,
        sum(total_payment)  as total_revenue,
        avg(total_payment)  as avg_order_value
    from orders
    where order_status = 'delivered'
    group by month
)

select * from monthly
order by month