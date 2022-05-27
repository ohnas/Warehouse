import os
import pandas as pd


def make_sample(upload_file, generated_path):
    # upload_file 의 경로를 가져와서 dirname 으로 파일명 제외하고 저장된 경로만 찾기
    if "smartstore" in os.path.dirname(upload_file):
        # 선택된 excel file 가져와서 Dataframe 으로 만들기
        row_df = pd.read_excel(f"{upload_file}", engine="openpyxl")

        # row_df 에서 원하는 column 만 가져오기
        select_df = row_df[
            [
                "주문번호",
                "수취인명",
                "옵션정보",
                "수량",
                "수취인연락처1",
                "수취인연락처2",
                "배송지",
                "배송메세지",
            ]
        ]
        # int64 type 을 astype() 메소드를 이용하여 objects type으로 변경
        select_df["주문번호"] = select_df["주문번호"].astype(str)

        # select_df 에서 column 위치조정
        relocation_df = select_df[
            [
                "주문번호",
                "수취인명",
                "배송지",
                "수취인연락처1",
                "수취인연락처2",
                "옵션정보",
                "수량",
                "배송메세지",
            ]
        ]

        # relocation_df 에서 column 이름 rename 하기
        rename_df = relocation_df.rename(
            columns={
                "주문번호": "고객주문번호",
                "수취인명": "받는분성명",
                "배송지": "받는분주소(전체,분할)",
                "수취인연락처1": "받는분전화번호",
                "수취인연락처2": "받는분기타연락처",
                "옵션정보": "품목명",
                "수량": "내품수량",
            }
        )
        # column insert 하기
        rename_df.insert(6, "내품명", "")

        # column 추가하기
        rename_df["운임구분"] = "신용"
        rename_df["박스타입"] = "극소"
        rename_df["기본운임"] = 2050
        rename_df["보내는분성명"] = "몬스터Monster"
        rename_df["보내는분주소(전체, 분할)"] = "인천 서구 가좌동 585-14 cj대한통운 인천가좌심곡대리점"
        rename_df["보내는분전화번호"] = "1522-8145"
        rename_df["보내는분기타연락처"] = ""

    return rename_df.to_excel(f"{generated_path}/cj_sample.xlsx", index=False)


def make_waybill(file1, file2):
    waybill_df = pd.read_excel(
        f"{file1}",
        engine="openpyxl",
    )

    select_waybill_df = waybill_df[["운송장번호", "받는분", "받는분 전화번호", "받는분주소"]]
    # int64 type 을 astype() 메소드를 이용하여 objects type으로 변경하고 모든 데이터에 일괄적으로 가장 앞에 '0' 붙여주기
    select_waybill_df["받는분 전화번호"] = "0" + select_waybill_df["받는분 전화번호"].astype(str)
    # merge 하기 위해서 기준 df에 있는 열 이름으로 통일시키기
    select_waybill_df = select_waybill_df.rename(
        columns={
            "받는분": "수취인명",
            "받는분 전화번호": "수취인연락처1",
            "받는분주소": "배송지",
        }
    )

    row_df = pd.read_excel(
        f"{file2}",
        engine="openpyxl",
    )

    select_row_df = row_df[["수취인명", "수취인연락처1", "배송지"]]
    # 전화번호 데이터 형식이 '000-0000-0000' 이므로 '-'를 제거
    select_row_df["수취인연락처1"] = select_row_df["수취인연락처1"].str.replace("-", "")
    # 기준 데이터와 비교데이터를 merge 해서 새로운 df로 생성 // merge 메소드는 excel의 vlookpu 과 같은 효과
    merge_df = select_row_df.merge(
        select_waybill_df, on=["수취인명", "수취인연락처1", "배송지"], how="left"
    )
    # merge 한 df 에서 특정 열(운송장번호)만 새롭게 생성
    df = merge_df[["운송장번호"]]

    with pd.ExcelWriter(
        f"{file2}",
        mode="a",
        engine="openpyxl",
        if_sheet_exists="overlay",
    ) as writer:
        df.to_excel(
            writer,
            sheet_name="발주발송관리",
            startcol=6,
            index=False,
        )
    return
