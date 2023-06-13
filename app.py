import gradio as gr
import json
import pandas as pd
import pickle
import logging
import os


MAIN_FOLDER = os.path.dirname(os.path.curdir)
MODEL_PATH = os.path.join(MAIN_FOLDER, "model/modelo_proyecto_final.pkl")
COLUMNS_PATH = os.path.join(MAIN_FOLDER, "model/categories_ohe_without_fraudulent.pickle")
BINS_ORDER = os.path.join(MAIN_FOLDER, "model/saved_bins_order.pickle")
BINS_TRANSACTION = os.path.join(MAIN_FOLDER, "model/saved_bins_transaction.pickle")

logging.info(f"MAIN_FOLDER: {MAIN_FOLDER}")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(COLUMNS_PATH, 'rb') as handle:
    ohe_tr = pickle.load(handle)

with open(BINS_ORDER, 'rb') as handle:
    new_saved_bins_order = pickle.load(handle)

with open(BINS_TRANSACTION, 'rb') as handle:
    new_saved_bins_transaction = pickle.load(handle)


def read_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def get_payment_method_issuer():
    return read_json_file('jsons/payment_method_issuer.json')


def get_payment_method_provider():
    return read_json_file('jsons/payment_method_provider.json')


# Define params names
PARAMS_NAME = [
    "orderAmount",
    "orderState",
    "paymentMethodRegistrationFailure",
    "paymentMethodType",
    "paymentMethodProvider",
    "paymentMethodIssuer",
    "transactionAmount",
    "transactionFailed",
    "emailDomain",
    "emailProvider",
    "customerIPAddressVersion",
    "sameCity"
]


def predict(*args):
    answer_dict = {}

    for i in range(len(PARAMS_NAME)):
        answer_dict[PARAMS_NAME[i]] = [args[i]]

    single_instance = pd.DataFrame.from_dict(answer_dict)

    # Manejar puntos de corte o bins
    single_instance["orderAmount"] = single_instance["orderAmount"].astype(float)
    single_instance["orderAmount"] = pd.cut(single_instance['orderAmount'],
                                            bins=new_saved_bins_order,
                                            include_lowest=True)

    single_instance["transactionAmount"] = single_instance["transactionAmount"].astype(int)
    single_instance["transactionAmount"] = pd.cut(single_instance['transactionAmount'],
                                                  bins=new_saved_bins_order,
                                                  include_lowest=True)

    # One hot encoding
    single_instance_ohe = pd.get_dummies(single_instance).reindex(columns=ohe_tr).fillna(0)

    prediction = model.predict(single_instance_ohe)
    type_of_fraud = int(prediction[0])

    # Adaptación respuesta
    response = "Error parsing value"
    if type_of_fraud == 0:
        response = "False"
    if type_of_fraud == 1:
        response = "True"
    if type_of_fraud == 2:
        response = "Warning"

    return response


with gr.Blocks() as demo:
    gr.Markdown(
        """
        # Prevención de Fraude 🙂😠
        """
    )

    with gr.Row():
        with gr.Column():
            gr.Markdown(
                """
                ## Predecir si un cliente es fraudulento o no
                """
            )

            order_amount = gr.Slider(label="Order Amount", minimum=0, maximum=500, step=1, randomize=True)

            order_state = gr.Radio(label="Order State", choices=["failed", "fulfilled", "pending"], value="fulfilled")

            payment_method_registration_failure = gr.Radio(label="Payment Method Registration Failure",
                                                           choices=["True", "False"], value="False")

            payment_method_type = gr.Radio(label="Payment Method Type",
                                           choices=["card", "apple pay", "paypal", "bitcoin"], value="card")

            payment_method_provider = gr.Dropdown(label="Payment Method Provider",
                                                  choices=get_payment_method_provider(),
                                                  multiselect=False, value="JCB 16 digit")

            payment_method_issuer = gr.Dropdown(label="Payment Method Issuer",
                                                choices=get_payment_method_issuer(),
                                                multiselect=False,
                                                value="Citizens First Banks")

            transaction_amount = gr.Slider(label="Transaction Amount", minimum=0, maximum=500, step=1, randomize=True)

            transaction_failed = gr.Radio(label="Transaction Failed", choices=["True", "False"], value="False")

            email_domain = gr.Radio(label="Email Domain",
                                    choices=["biz", "com", "info", "net", "org", "weird"],
                                    value="com")

            email_provider = gr.Radio(label="Email Provider",
                                      choices=["gmail", "hotmail", "yahoo", "weird", "other"],
                                      value="gmail")

            customer_ip_address_version = gr.Radio(label="Customer IP Address Version",
                                                   choices=["4.0", "6.0"],
                                                   value="4.0")

            same_city = gr.Radio(label="Same City",
                                 choices=["no", "yes", "unknown"],
                                 value="yes")

        with gr.Column():
            gr.Markdown(
                """
                ## Predicción
                """
            )

            label = gr.Label(label="Tipo Fraude")
            predict_btn = gr.Button(value="Evaluar")
            predict_btn.click(
                predict,
                inputs=[
                    order_amount,
                    order_state,
                    payment_method_registration_failure,
                    payment_method_type,
                    payment_method_provider,
                    payment_method_issuer,
                    transaction_amount,
                    transaction_failed,
                    email_domain,
                    email_provider,
                    customer_ip_address_version,
                    same_city
                ],
                outputs=[label],
                api_name="prediccion"
            )
    gr.Markdown(
        """
            <p style='text-align: center'>
                <a href='https://www.escueladedatosvivos.ai/cursos/bootcamp-de-data-science' 
                      target='_blank'>Proyecto demo creado en el bootcamp de EDVAI 🤗
                </a>
            </p>
        """
    )

demo.launch()

