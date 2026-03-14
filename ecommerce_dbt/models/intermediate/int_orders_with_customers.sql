with orders as (
    select * 
    from {{ ref('int_orders_with_payments') }}
),

customers as (
    select * 
    from {{ ref('stg_customers') }}
)

select
    o.*,
    c.customer_unique_id,
    c.city  as customer_city,
    c.state as customer_state,
    c.zip_code  as customer_zip_code
from orders o
left join customers c using (customer_id)