"""실습 날짜와 시드를 고정하고 예약 시각을 만든다."""
from datetime import date, timedelta

TODAY = '2026-10-27'
SEED = 37


def checked_today(value=TODAY):
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as error:
        raise ValueError('날짜 오류 → --today 2026-10-27 형식으로 고치세요') from error


def scheduled_date(today=TODAY):
    return (date.fromisoformat(checked_today(today)) + timedelta(days=1)).isoformat() + 'T09:00:00'
