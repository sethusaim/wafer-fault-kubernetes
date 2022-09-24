from yaml import safe_load


def read_params(config_path="params.yaml"):
    """
    Method Name :   read_params
    Description :   This method reads the parameters from params.yaml file

    Output      :   Parameters are read from the params.yaml file
    On Failure  :   Write an exception log and then raise an exception

    Version     :   1.2
    Revisions   :   moved setup to cloud
    """
    method_name = read_params.__name__

    try:
        with open(config_path) as f:
            config = safe_load(f)

        return config

    except Exception as e:
        raise Exception(
            f"Exception occured in {__file__}, Method : {method_name}, Error : {str(e)}"
        )


def get_log_dic(class_name, method_name, file):
    """
    Method Name :   get_log_dic
    Description :   This method gets extra log params as dict
    Output      :   Parameters are read from the params.yaml file
    On Failure  :   Write an exception log and then raise an exception
    Version     :   1.2
    Revisions   :   moved setup to cloud
    """
    _method_name = get_log_dic.__name__

    try:
        log_dic = {
            "class_name": class_name,
            "method_name": method_name,
            "file": file,
            "log_file": log_file,
        }

        return log_dic

    except Exception as e:
        raise Exception(
            f"Exception occured in {__file__}, Method : {_method_name}, Error : {str(e)}"
        )
