import streamlit as st
import requests
from requests.exceptions import RequestException

st.set_page_config(page_title="Railway Ticket Management", layout="wide")

st.title("Railway Ticket Management System")

base_url = st.text_input("API base URL", value="http://127.0.0.1:8000")


def request_json(method, path, payload=None):
    url = f"{base_url}{path}"
    try:
        resp = requests.request(method, url, json=payload, timeout=10)
        if resp.status_code >= 400:
            try:
                detail = resp.json().get("detail", resp.text)
            except ValueError:
                detail = resp.text
            return None, f"{resp.status_code}: {detail}"
        if resp.text:
            return resp.json(), None
        return {}, None
    except RequestException as exc:
        return None, str(exc)


train_tab, booking_tab, admin_tab = st.tabs(["Trains", "Bookings", "Admin"])

with train_tab:
    st.subheader("Browse Trains")
    if st.button("Load trains"):
        data, err = request_json("GET", "/trains")
        if err:
            st.error(err)
        else:
            st.dataframe(data, use_container_width=True)

    st.subheader("Train details")
    train_id = st.number_input("Train ID", min_value=1, step=1, value=1, key="details_train_id")
    if st.button("Fetch train details"):
        data, err = request_json("GET", f"/trains/{int(train_id)}")
        if err:
            st.error(err)
        else:
            st.json(data)

with booking_tab:
    st.subheader("Book a ticket")
    with st.form("book_form"):
        user_name = st.text_input("User name", value="")
        train_id = st.number_input("Train ID", min_value=1, step=1, value=1, key="book_train_id")
        class_type = st.text_input("Class type", value="SL")
        submitted = st.form_submit_button("Book")
        if submitted:
            payload = {
                "user_name": user_name.strip(),
                "train_id": int(train_id),
                "class_type": class_type.strip(),
            }
            data, err = request_json("POST", "/book", payload)
            if err:
                st.error(err)
            else:
                st.success("Booking created")
                st.json(data)

    st.subheader("Cancel a ticket")
    with st.form("cancel_form"):
        pnr = st.text_input("PNR", value="")
        cancel = st.form_submit_button("Cancel")
        if cancel:
            data, err = request_json("POST", f"/cancel/{pnr.strip()}")
            if err:
                st.error(err)
            else:
                st.success("Ticket cancelled")
                st.json(data)

    st.subheader("User bookings")
    with st.form("list_bookings_form"):
        user_query = st.text_input("User name", value="")
        list_submit = st.form_submit_button("Load bookings")
        if list_submit:
            data, err = request_json("GET", f"/bookings/{user_query.strip()}")
            if err:
                st.error(err)
            else:
                st.dataframe(data, use_container_width=True)

with admin_tab:
    st.subheader("Create train")
    with st.form("create_train_form"):
        col1, col2 = st.columns(2)
        with col1:
            train_number = st.text_input("Train number", value="")
            train_name = st.text_input("Train name", value="")
        with col2:
            source = st.text_input("Source", value="")
            destination = st.text_input("Destination", value="")

        class_count = st.number_input("Number of classes", min_value=1, max_value=5, step=1, value=1)
        classes = []
        for i in range(int(class_count)):
            st.markdown(f"Class {i + 1}")
            c1, c2, c3 = st.columns(3)
            with c1:
                class_type = st.text_input("Class type", value="SL", key=f"class_type_{i}")
            with c2:
                total_seats = st.number_input("Total seats", min_value=1, step=1, value=100, key=f"total_{i}")
            with c3:
                available_seats = st.number_input(
                    "Available seats", min_value=0, step=1, value=100, key=f"avail_{i}"
                )
            classes.append(
                {
                    "class_type": class_type.strip(),
                    "total_seats": int(total_seats),
                    "available_seats": int(available_seats),
                }
            )

        submit_train = st.form_submit_button("Create train")
        if submit_train:
            payload = {
                "train_number": train_number.strip(),
                "train_name": train_name.strip(),
                "source": source.strip(),
                "destination": destination.strip(),
                "classes": classes,
            }
            data, err = request_json("POST", "/trains", payload)
            if err:
                st.error(err)
            else:
                st.success("Train created")
                st.json(data)
