from evaluator.utils.const import const

const.PUBLIC = 1
const.PRIVATE = 2
const.PROTECTED = 4
const.STATIC = 8
const.FINAL = 16
const.SYNCHRONIZED = 32
const.VOLATILE = 64
const.TRANSIENT = 128
const.NATIVE = 256
const.SEALED = 512
const.ABSTRACT = 1024
const.STRICTFP = 2048


def _get_modifiers_number():
    return {'public': const.PUBLIC, 'private': const.PRIVATE, 'protected': const.PROTECTED, 'static': const.STATIC,
            'final': const.FINAL, 'synchronized': const.SYNCHRONIZED, 'volatile': const.VOLATILE,
            'transient': const.TRANSIENT, 'native': const.NATIVE, 'sealed': const.SEALED, 'abstract': const.ABSTRACT,
            'strictfp': const.STRICTFP}


def get_modifiers(entity):
    c_modifiers = 0
    if 'modifiers' in entity:
        modifier_list = entity['modifiers'].split(' ')
        for modifier in modifier_list:
            if modifier in _get_modifiers_number():
                c_modifiers += _get_modifiers_number()[modifier]
    return c_modifiers


def judge_modifier_type(entity, public_num, protected_num, private_num, static_num, default_num, final_num, synchronized_num, abstrcat_num):
    if 'modifiers' not in entity:
        default_num += 1
    else:
        if 'public' in entity['modifiers']:
            public_num += 1
        if 'protected' in entity['modifiers']:
            protected_num += 1
        if 'private' in entity['modifiers']:
            private_num += 1
        if 'static' in entity['modifiers']:
            static_num += 1
            if 'public' not in entity['modifiers'] and 'protected' not in entity['modifiers'] and 'private' not in entity['modifiers']:
                default_num += 1
        if 'default' in entity['modifiers']:
            default_num += 1
        if 'final' in entity['modifiers']:
            final_num += 1
        if 'synchronized' in entity['modifiers']:
            synchronized_num += 1
        if 'abstract' in entity['modifiers']:
            abstrcat_num += 1

    return public_num, protected_num, private_num, static_num, default_num, final_num, synchronized_num, abstrcat_num
