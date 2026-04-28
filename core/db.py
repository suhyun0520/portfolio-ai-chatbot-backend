import psycopg2

def save_chat_log(
    database_url: str | None,
    visitor_id: str | None,
    user_agent: str | None,
    question: str,
    answer: str,
    model: str | None = None,
) -> None:
    if not database_url:
        print("DATABASE_URL is not set. Skip chat log save.")
        return
    
    try:
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO chat_logs
                    (visitor_id, user_agent, question, answer, model)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        visitor_id,
                        user_agent,
                        question,
                        answer,
                        model,
                    ),
                )
    except Exception as e:
        print("chat log save failed:", e)


