with orders as (
    select * from {{ ref('int_orders_with_customers') }}
),

delivery as (
    select
        customer_state,
        count(distinct order_id)    as total_orders,
        avg(extract(epoch from (delivered_at - purchased_at)) / 86400)  as avg_delivery_days,
        avg(extract(epoch from (estimated_delivery_at - delivered_at)) / 86400)   as avg_days_early_or_late
    from orders
    where order_status = 'delivered'
    and delivered_at is not null
    group by 1
)

select * from delivery
order by avg_delivery_days