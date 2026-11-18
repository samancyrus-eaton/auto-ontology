from pathlib import Path

import duckdb


DATA_FILE = (
    Path(__file__).resolve().parent
    / "data"
    / "CAB760M12HM3_GRIDDED_REMOVAL_PD1_together.parquet"
)
POINT_IDS = (313346, 313405)


def main() -> None:
    if not DATA_FILE.is_file():
        raise SystemExit(f"Parquet file not found: {DATA_FILE}")

    query = """
        SELECT point_id, total_losses
        FROM read_parquet(?)
        WHERE point_id IN (?, ?)
        ORDER BY point_id
    """
    with duckdb.connect() as connection:
        rows = connection.execute(query, [str(DATA_FILE), *POINT_IDS]).fetchall()

    if len(rows) != len(POINT_IDS):
        found = [int(point_id) for point_id, _ in rows]
        raise SystemExit(
            f"Expected one row for each point_id {POINT_IDS}; found {found}"
        )

    values = {int(point_id): total_losses for point_id, total_losses in rows}
    for point_id in POINT_IDS:
        print(f"point_id={point_id} total_losses={values[point_id]}")

    difference = values[POINT_IDS[1]] - values[POINT_IDS[0]]
    print(
        f"difference ({POINT_IDS[1]} - {POINT_IDS[0]})="
        f"{difference}"
    )


if __name__ == "__main__":
    main()
