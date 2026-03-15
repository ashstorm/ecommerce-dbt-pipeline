with orders as (
    select * from {{ ref('int_orders_with_customers') }}
),

customer_stats as (
    select
        customer_unique_id,
        customer_city,
        customer_state,
        count(distinct order_id)    as total_orders,
        sum(total_payment)  as total_spent,
        avg(total_payment)  as avg_order_value,
        min(purchased_at)   as first_order_at,
        max(purchased_at)   as last_order_at
    from orders
    where order_status = 'delivered'
    group by 1, 2, 3 --here this just means that we are grouping by the first 3 columns in the select statement
),

segmented as (
    select *,
        case
            when total_spent >= 1000 then 'High Value'
            when total_spent >= 500  then 'Mid Value'
            else 'Low Value'
        end as customer_segment
    from customer_stats
)

select * from segmented
order by total_spent desc