with products as (
    select * 
    from {{ ref('stg_products') }}
),

translations as (
    select * 
    from {{ source('raw', 'raw_name_translations') }}
)

select
    p.*,t.product_category_name_english  as category_name_english
from products p
left join translations t on p.category_name = t.product_category_name