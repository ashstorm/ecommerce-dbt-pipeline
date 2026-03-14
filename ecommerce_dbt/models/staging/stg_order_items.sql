with source as (
    select * from {{ source('raw', 'raw_order_items')}}
),

cleaned as (
    select
        order_id,
        order_item_id,
        product_id,
        seller_id,
        price,
        freight_value,
        cast(shipping_limit_date as TIMESTAMP) as shipping_limit_at
    from source
)

select * from cleaned