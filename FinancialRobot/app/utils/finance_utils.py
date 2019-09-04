from decimal import Decimal


def capitalized_amount_of_money(amount):
    amount = round(amount, 2)
    amount_strs = str(amount).split('.')
    # 转换的最大位数
    # 只能识别亿级及以下的
    max_mag = 9
    if amount > 10**max_mag:
        return '.'.join(amount_strs)
    print(amount_strs)
    # 每种数字对应大写
    digit_li = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
    # 每个位置上的单位
    units = ['亿', '仟', '佰', '拾', '万', '仟', '佰', '拾', '元', '角', '分']
    ten_thousand_pos = 4
    amount_strs[0] = amount_strs[0].zfill(9)
    amount_cap = ''
    for i in range(len(amount_strs[0])):
        char = amount_strs[0][i]
        unit = units[i]
        digit_cap = digit_li[int(char)]
        if amount_cap and i == ten_thousand_pos+1 and amount_strs[0][i-1] == '0':
            # 若万及以上的位数已扫描完毕且万以上不为0，检查是否已 万 为单位结尾
            amount_cap = amount_cap + units[ten_thousand_pos]
        if char == '0':
            # 为0略过
            continue
        if i > 0 and amount_strs[0][i-1] == '0' and amount_cap:
            # 若当前数字为隔了数个0之后出现的非零数字
            amount_cap = amount_cap + '零'
        amount_cap = amount_cap + digit_cap + unit
    if amount_strs[0][max_mag-1] == '0':
        amount_cap += units[max_mag-1]
    dot_cap = ''
    if len(amount_strs) > 1:
        for i in range(len(amount_strs[1])):
            char = amount_strs[1][i]
            unit = units[9+i]
            digit_cap = digit_li[int(char)]
            if char == '0':
                continue
            if i > 0 and amount_strs[1][i-1] == '0' and dot_cap:
                dot_cap = dot_cap + '零'
            dot_cap = dot_cap + digit_cap + unit
    else:
        amount_cap = amount_cap + '整'
    if not dot_cap:
        amount_cap = amount_cap + '整'
    else:
        amount_cap = amount_cap + dot_cap
    return amount_cap


def remove_exponent(num):
    num = Decimal(num)
    return num.to_integral() if num == num.to_integral() else num.normalize()


def magnitude_digit(num, mag):
    if num < 10**mag:
        return ''
    num = remove_exponent(num)
    num_strs = str(num).split('.')
    if mag >= 0:
        return num_strs[0][-(mag+1)]
    else:
        if len(num_strs) > 1 and len(num_strs[1]) >= -mag:
            return num_strs[1][-(mag+1)]
        else:
            return ''
