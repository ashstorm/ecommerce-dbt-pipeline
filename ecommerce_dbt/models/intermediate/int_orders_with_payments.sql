with orders as (
    select *
    from {{ ref('stg_orders') }}
),

payments as (
    select
        order_id,
        sum(payment_value) as total_payment,
        count(payment_sequential) as payment_count,
        max(payment_type) as payment_type,
        max(payment_installments) as payment_installments
    from {{ ref('stg_payments') }}
    group by order_id
)

select
    o.*,
    p.total_payment,
    p.payment_count,
    p.payment_type,
    p.payment_installments
from orders o
left join payments p using (order_id)