"""
    Crea formularios de manera dinamica
"""
from flask_wtf import FlaskForm
from wtforms import (ValidationError,
                     SelectField, StringField, validators, DecimalField, IntegerField)


async def build_form(vars: list) -> FlaskForm:
    """Encagrado de crrear formularios dinamicos mediante una lista de objestos {
        'label':valor,
        'requires':bool,
        etc
    }
    """

    class BaseForm(FlaskForm):
        """Formulario vacio de FlaskForms"""
        ...
    
    def numeric_field(base_class, label: str = '', validators: list = [], restrictions: list = [], **kwargs):

        __class__: dict = {
            'float': DecimalField,
            'int': IntegerField
        }

        class NumericField(__class__[base_class]):
            """Field numerico personalizado"""

            def __init__(self, label: str = '', validators: list = [], restrictions: list = [], **kwargs):
                super(NumericField, self).__init__(label, validators, **kwargs)
                self.restrictions: list = restrictions

            def pre_validate(self, form):
                super(NumericField, self).pre_validate(form)
                if self.data is not None and not self.custom_validation(self.data):
                    raise ValidationError(', '.join(self.restrictions))

            def process_formdata(self, valuelist):
                if valuelist:
                    self.data = valuelist[0]

            def custom_validation(self, value):
                """Evalua las reglas establecidas en el archivo config"""
                passed: list = [False] * len(self.restrictions)
                for index, restriction in enumerate(self.restrictions):
                    passed[index] = eval(f'{value}{restriction}')
                return all(passed)

        return NumericField(label, validators, restrictions, **kwargs)

    def __build_numeric__(id_name: str, required: bool, args):
        type_number: str = args.pop("specific_type")

        if required:
            field = numeric_field(base_class=type_number, validators=[validators.DataRequired()],
                                  **args)
            setattr(BaseForm, id_name.strip(), field)
        else:
            field = numeric_field(base_class=type_number, **args)
            setattr(BaseForm, id_name.strip(), field)

    def __build_options__(id_name: str, required: bool, args):
        setattr(BaseForm, id_name.strip(), SelectField(**args), )

    def __build_string__(id_name: str, required: bool, args):
        if required:
            setattr(BaseForm, id_name.strip(), StringField(validators=[validators.DataRequired()],
                                                           **args), )
        else:
            setattr(BaseForm, id_name.strip(), StringField(**args))

    types: dict = {
        'numeric': __build_numeric__,
        'string': __build_string__,
        'options': __build_options__
    }

    for var in vars:
        var_type: str = var.pop('type')
        required: str = var.pop('required')
        id_name: str = var.get('label')
        types[var_type](id_name=id_name,
                        required=required,
                        args=var)

    return BaseForm()
