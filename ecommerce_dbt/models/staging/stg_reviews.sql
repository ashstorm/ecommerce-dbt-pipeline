with source as (
    select * from {{source('raw','raw_reviews')}}
),

cleaned as (
    select
        review_id,
        order_id,
        review_score,
        review_comment_title    as comment_title,
        review_comment_message  as comment_message,
        cast(review_creation_date as TIMESTAMP) as created_at,
        cast(review_answer_timestamp as TIMESTAMP)  as answered_at
    from source
)

select * from cleaned