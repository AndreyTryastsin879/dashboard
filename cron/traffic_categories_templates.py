import pandas as pd

FOLDER_PATH = 'projects_aliases'

def megaposm(df):
    main = 'https://megaposm.com/'
    cat = df['urls'].str.contains(pat='https://megaposm.com/.*/$',regex=True)
    subdomain = df['urls'].str.contains(pat='https://.*[A-z].megaposm.com/.*',regex=True)
    
    df['traffic_category'] = ''
    df.loc[df['urls'] == main, 'traffic_category'] = 'Главная'
    df.loc[df['urls'].isin(df[cat]['urls']), 'traffic_category'] = 'Категории'
    df.loc[df['urls'].isin(df[subdomain]['urls']), 'traffic_category'] = 'Региональные поддомены'
    df['traffic_category'] = df['traffic_category'].replace('', 'Карточки товаров')
    df.sort_values(by = 'visits_quantity', ascending = False, inplace = True) 

    df_pivot = df.pivot_table(index='traffic_category', values='visits_quantity', aggfunc='sum').reset_index()
    
    df_pivot = df_pivot.to_dict('record')

    return df_pivot


def frutoss(df):
    frutoss_categories_aliases = pd.read_csv(f'{FOLDER_PATH}/frutoss_categories_aliases.csv')
    frutoss_products_aliases = pd.read_csv(f'{FOLDER_PATH}/frutoss_products_aliases.csv')

    main = 'https://frutoss.ru/'
    subdomain = df['urls'].str.contains(pat='https://.*[A-z].frutoss.ru/.*',regex=True)
    recipe = df['urls'].str.contains(pat='https://frutoss.ru/.*-retsept$',regex=True)
    blog = df['urls'].str.contains(pat='https://frutoss.ru/.*-blog$',regex=True)
    
    df['traffic_category'] = ''
    df['splitted_url'] = df['urls'].apply(lambda x: x.split('/'))
    df['only_alias'] = df['splitted_url'].apply(lambda x: x[len(x)-1])
    
    df.loc[df['urls'] == main, 'traffic_category'] = 'Главная'
    
    df.loc[df['only_alias'].isin(frutoss_categories_aliases['alias']), 'traffic_category'] = 'Категории'
    df.loc[df['only_alias'].isin(frutoss_products_aliases['alias']), 'traffic_category'] = 'Карточки'
    
    df.loc[df['urls'].isin(df[subdomain]['urls']), 'traffic_category'] = 'Региональные поддомены'
    df.loc[df['urls'].isin(df[recipe]['urls']), 'traffic_category'] = 'Рецепты'
    df.loc[df['urls'].isin(df[blog]['urls']), 'traffic_category'] = 'Статьи'
    df['traffic_category'] = df['traffic_category'].replace('', 'Другое')

    df.sort_values(by = 'visits_quantity', ascending = False, inplace = True) 

    df_pivot = df.pivot_table(index='traffic_category', values='visits_quantity', aggfunc='sum').reset_index()
    
    df_pivot = df_pivot.to_dict('record')

    return df_pivot


def mentalshop(df):
    main = 'https://mentalshop.ru/'
    cat = df['urls'].str.contains(pat='https://mentalshop.ru/.*/$',regex=True)
    card = df['urls'].str.contains(pat='https://mentalshop.ru/.*/.*.html$',regex=True)
    subdomain = df['urls'].str.contains(pat='https://.*[a-z].mentalshop.ru/.*',regex=True)
    
    brand_pat = df['urls'].str.contains(pat='https://mentalshop.ru/.*.html$',regex=True)
    brand_pages = df[(brand_pat) & ~(card)]
    
    df['traffic_category'] = ''
    df.loc[df['urls'] == main, 'traffic_category'] = 'Главная'
    df.loc[df['urls'].isin(df[cat]['urls']), 'traffic_category'] = 'Категории'
    df.loc[df['urls'].isin(df[card]['urls']), 'traffic_category'] = 'Карточки товаров'
    df.loc[df['urls'].isin(df[subdomain]['urls']), 'traffic_category'] = 'Региональные поддомены'
    df.loc[df['urls'].isin(brand_pages['urls']), 'traffic_category'] = 'Страницы брендов'
    df['traffic_category'] = df['traffic_category'].replace('', 'Другое')
    
    df.sort_values(by = 'visits_quantity', ascending = False, inplace = True) 

    df_pivot = df.pivot_table(index='traffic_category', values='visits_quantity', aggfunc='sum').reset_index()
    
    df_pivot = df_pivot.to_dict('record')

    return df_pivot


def davita(df):
    main = 'https://da-vita.ru/'
    cat = df['urls'].str.contains(pat='https://da-vita.ru/catalog/.*.html',regex=True)
    card = df['urls'].str.contains(pat='https://da-vita.ru/catalog/.*/.*.html',regex=True)
    blog = df['urls'].str.contains(pat='https://da-vita.ru/beauty-blog/.*.html',regex=True)
    faq = df['urls'].str.contains(pat='https://da-vita.ru/faq/.*.html',regex=True)
    review = df['urls'].str.contains(pat='https://da-vita.ru/otzyvy-o-kosmetike/.*.html',regex=True)
    subdomain = df['urls'].str.contains(pat='https://.*[a-z].da-vita.ru/.*',regex=True)
    cat_pages = df[(cat) & ~(card)]
    
    df['traffic_category'] = ''
    df.loc[df['urls'] == main, 'traffic_category'] = 'Главная'
    df.loc[df['urls'].isin(cat_pages['urls']), 'traffic_category'] = 'Категории'
    df.loc[df['urls'].isin(df[card]['urls']), 'traffic_category'] = 'Карточки'
    df.loc[df['urls'].isin(df[subdomain]['urls']), 'traffic_category'] = 'Региональные поддомены'
    df.loc[df['urls'].isin(df[blog]['urls']), 'traffic_category'] = 'Блог'
    df.loc[df['urls'].isin(df[faq]['urls']), 'traffic_category'] = 'FAQ'
    df.loc[df['urls'].isin(df[review]['urls']), 'traffic_category'] = 'Отзывы'
    df['traffic_category'] = df['traffic_category'].replace('', 'Другие страницы')
    
    df.sort_values(by = 'visits_quantity', ascending = False, inplace = True) 

    df_pivot = df.pivot_table(index='traffic_category', values='visits_quantity', aggfunc='sum').reset_index()
    
    df_pivot = df_pivot.to_dict('record')
    
    return df_pivot


def guinot(df):
    main = 'https://guinot-salon.ru/'
    catalog = 'https://guinot-salon.ru/products/'
    pricelist = 'https://guinot-salon.ru/pricelist/'
    cat = df['urls'].str.contains(pat='.*guinot-salon.ru/products/.*/$',regex=True)
    card = df['urls'].str.contains(pat='.*guinot-salon.ru/products/.*/.*.html$',regex=True)
    service = df['urls'].str.contains(pat='.*guinot-salon.ru/services/.*',regex=True)
    blog = df['urls'].str.contains(pat='.*guinot-salon.ru/blog/.*',regex=True)

    df['traffic_category'] = ''
    df.loc[df['urls'] == main, 'traffic_category'] = 'Главная'
    df.loc[df['urls'] == catalog, 'traffic_category'] = 'Интернет-магазин главная'
    df.loc[df['urls'].isin(df[cat]['urls']), 'traffic_category'] = 'Категории'
    df.loc[df['urls'].isin(df[card]['urls']), 'traffic_category'] = 'Карточки товаров'
    df.loc[df['urls'] == pricelist, 'traffic_category'] = 'Услуги прайс-лист'
    df.loc[df['urls'].isin(df[service]['urls']), 'traffic_category'] = 'Услуги подробно'
    df.loc[df['urls'].isin(df[blog]['urls']), 'traffic_category'] = 'Статьи'
    
    df['traffic_category'] = df['traffic_category'].fillna('Другие страницы')
    
    df.sort_values(by = 'visits_quantity', ascending = False, inplace = True)
    
    df_pivot = df.pivot_table(index='traffic_category', values='visits_quantity', aggfunc='sum').reset_index()
    
    df_pivot = df_pivot.to_dict('record')
    
    return df_pivot


def bigbears(df):
    bigbears_categories_aliases = pd.read_csv('projects_aliases/bigbears_categories_aliases.csv')
    bigbears_products_aliases = pd.read_csv('projects_aliases/bigbears_products_aliases.csv')

    main = 'https://big-bears.ru/'
    subdomain = df['urls'].str.contains(pat='https://.*[A-z].big-bears.ru/.*',regex=True)
    blog = df['urls'].str.contains(pat='https://big-bears.ru/index.php?route=simple_blog/article/.*',regex=True)
    
    df['traffic_category'] = ''
    df['splitted_url'] = df['urls'].apply(lambda x: x.split('/'))
    df['only_alias'] = df['splitted_url'].apply(lambda x: x[len(x)-1])
    
    df.loc[df['urls'] == main, 'traffic_category'] = 'Главная'
    
    df.loc[df['only_alias'].isin(bigbears_categories_aliases['alias']), 'traffic_category'] = 'Категории'
    df.loc[df['only_alias'].isin(bigbears_products_aliases['alias']), 'traffic_category'] = 'Карточки'
    
    df.loc[df['urls'].isin(df[subdomain]['urls']), 'traffic_category'] = 'Региональные поддомены'
    df.loc[df['urls'].isin(df[blog]['urls']), 'traffic_category'] = 'Статьи'
    df['traffic_category'] = df['traffic_category'].replace('', 'Другое')

    df.sort_values(by = 'visits_quantity', ascending = False, inplace = True) 

    df_pivot = df.pivot_table(index='traffic_category', values='visits_quantity', aggfunc='sum').reset_index()
    
    df_pivot = df_pivot.to_dict('record')

    return df_pivot


def flexfit(df):
    main = 'https://flexfit.spb.ru/'
    card = df['urls'].str.contains(pat='https://flexfit.spb.ru/.*/.*',regex=True)
    subdomain = df['urls'].str.contains(pat='https://.*[a-z].flexfit.spb.ru/.*',regex=True)
    caps = 'https://flexfit.spb.ru/flexfit-caps'
    hats = 'https://flexfit.spb.ru/flexfit-hats'
    service = 'https://flexfit.spb.ru/branding'
        
    df['traffic_category'] = ''
    df.loc[df['urls'] == main, 'traffic_category'] = 'Главная'
    df.loc[df['urls'].isin(df[card]['urls']), 'traffic_category'] = 'Карточки товаров'
    df.loc[df['urls'].isin(df[subdomain]['urls']), 'traffic_category'] = 'Региональные поддомены'
    df.loc[df['urls'] == caps, 'traffic_category'] = 'Категория кепки'
    df.loc[df['urls'] == hats, 'traffic_category'] = 'Категория шапки'
    df.loc[df['urls'] == service, 'traffic_category'] = 'Брендирование'
    
    df['traffic_category'] = df['traffic_category'].replace('', 'Другое')
    
    df.sort_values(by = 'visits_quantity', ascending = False, inplace = True) 

    df_pivot = df.pivot_table(index='traffic_category', values='visits_quantity', aggfunc='sum').reset_index()
    
    df_pivot = df_pivot.to_dict('record')

    return df_pivot


def certex(df):
    certex = pd.read_excel(f'{FOLDER_PATH}/certex.xlsx')
    df = pd.merge(df, certex, on = 'urls', how='left')
    subdomain = df['urls'].str.contains(pat='https://.*[a-z].certex.spb.ru/.*',regex=True)
    
    df.loc[df['urls'].isin(df[subdomain]['urls']), 'traffic_category'] = 'Региональные поддомены'
    df['traffic_category'] = df['traffic_category'].fillna('Другое')
      
    df.sort_values(by = 'visits_quantity', ascending = False, inplace = True) 

    df_pivot = df.pivot_table(index='traffic_category', values='visits_quantity', aggfunc='sum').reset_index()
    
    df_pivot = df_pivot.to_dict('record')

    return df_pivot


def inauto(df):
    service_by_nissan_model = df['urls'].str.contains(pat='https://inautospb.ru/uslugi/remont-nissan.*',regex=True)
    service_by_infiniti_model = df['urls'].str.contains(pat='https://inautospb.ru/uslugi/remont-infiniti.*',regex=True)
    calc_filter = df['urls'].str.contains(pat='https://inautospb.ru/clc/.*',regex=True)
    
    main = 'https://inautospb.ru/'
    kalkulator = 'https://inautospb.ru/kalkulyator-to'
    tehnicheskoe_osluzhivanie = 'https://inautospb.ru/uslugi/tekhnicheskoe-obsluzhivanie'
    diagnostika = 'https://inautospb.ru/uslugi/diagnostika-avto-nissan-infiniti'
    kuzovnoj_remont = 'https://inautospb.ru/uslugi/kuzovnoj-remont'
    zamena_masla_kpp = 'https://inautospb.ru/uslugi/zamena-masla-v-akpp-mkpp'
    remont_dvigatelya = 'https://inautospb.ru/uslugi/remont-dvigatelya'
    zamena_masla_dvigatel = 'https://inautospb.ru/uslugi/zamena-masla-v-dvigatele'
    remont_podveski = 'https://inautospb.ru/uslugi/remont-podveski'
    remont_rulevogo = 'https://inautospb.ru/uslugi/remont-rulevogo-upravleniya'
    remont_elektriki = 'https://inautospb.ru/uslugi/remont-elektriki'
    
    df['traffic_category'] = ''
    df.loc[df['urls'].isin(df[service_by_nissan_model]['urls']), 'traffic_category'] = 'Услуги по моделям Ниссан'
    df.loc[df['urls'].isin(df[service_by_infiniti_model]['urls']), 'traffic_category'] = 'Услуги по моделям Инфинити'
    df.loc[df['urls'].isin(df[calc_filter]['urls']), 'traffic_category'] = 'Калькулятор фильтры'
    
    df.loc[df['urls'] == main, 'traffic_category'] = 'Главная'
    df.loc[df['urls'] == kalkulator, 'traffic_category'] = 'Калькулятор'
    
    df.loc[df['urls'] == tehnicheskoe_osluzhivanie, 'traffic_category'] = 'Услуги общ.'
    df.loc[df['urls'] == diagnostika, 'traffic_category'] = 'Услуги общ.'
    df.loc[df['urls'] == kuzovnoj_remont, 'traffic_category'] = 'Услуги общ.'
    df.loc[df['urls'] == zamena_masla_kpp, 'traffic_category'] = 'Услуги общ.'
    df.loc[df['urls'] == remont_dvigatelya, 'traffic_category'] = 'Услуги общ.'
    df.loc[df['urls'] == zamena_masla_dvigatel, 'traffic_category'] = 'Услуги общ.'
    df.loc[df['urls'] == remont_podveski, 'traffic_category'] = 'Услуги общ.'
    df.loc[df['urls'] == remont_rulevogo, 'traffic_category'] = 'Услуги общ.'
    df.loc[df['urls'] == remont_elektriki, 'traffic_category'] = 'Услуги общ.'

    df['traffic_category'] = df['traffic_category'].replace('', 'Другое')
    
    df.sort_values(by = 'visits_quantity', ascending = False, inplace = True) 

    df_pivot = df.pivot_table(index='traffic_category', values='visits_quantity', aggfunc='sum').reset_index()
    
    df_pivot = df_pivot.to_dict('record')

    return df_pivot


def skurala(df):
    skurala_categories_aliases = pd.read_csv(f'{FOLDER_PATH}/skurala_categories_aliases.csv')
    skurala_products_aliases = pd.read_csv(f'{FOLDER_PATH}/skurala_products_aliases.csv')

    main = 'https://skurala.ru/'
    
    df['traffic_category'] = ''
    df['splitted_url'] = df['urls'].apply(lambda x: x.split('/'))
    df['only_alias'] = df['splitted_url'].apply(lambda x: x[len(x)-2])
    
    df.loc[df['urls'] == main, 'traffic_category'] = 'Главная'
    
    df.loc[df['only_alias'].isin(skurala_categories_aliases['alias']), 'traffic_category'] = 'Категории'
    df.loc[df['only_alias'].isin(skurala_products_aliases['alias']), 'traffic_category'] = 'Карточки'
    
    df['traffic_category'] = df['traffic_category'].replace('', 'Другое')

    df.sort_values(by = 'visits_quantity', ascending = False, inplace = True) 

    df_pivot = df.pivot_table(index='traffic_category', values='visits_quantity', aggfunc='sum').reset_index()
    
    df_pivot = df_pivot.to_dict('record')

    return df_pivot


def elitewheels(df):
    elitewheels_categories_aliases = pd.read_csv(f'{FOLDER_PATH}/ew_categories_aliases.csv')
    elitewheels_products_aliases = pd.read_csv(f'{FOLDER_PATH}/ew_products_aliases.csv')
    elitewheels_filters_aliases = pd.read_csv(f'{FOLDER_PATH}/ew_filters_aliases.csv')

    main = 'https://elitewheels.ru/'
    
    df['traffic_category'] = ''
    df['splitted_url'] = df['urls'].apply(lambda x: x.split('/'))
    df['only_alias'] = df['splitted_url'].apply(lambda x: x[len(x)-1])
    
    df.loc[df['urls'] == main, 'traffic_category'] = 'Главная'
    
    df.loc[df['only_alias'].isin(elitewheels_categories_aliases['alias']), 'traffic_category'] = 'Категории'
    df.loc[df['only_alias'].isin(elitewheels_products_aliases['alias']), 'traffic_category'] = 'Карточки'
    df.loc[df['only_alias'].isin(elitewheels_filters_aliases['alias']), 'traffic_category'] = 'Фильтры'

    df['traffic_category'] = df['traffic_category'].replace('', 'Другое')

    df.sort_values(by = 'visits_quantity', ascending = False, inplace = True) 

    df_pivot = df.pivot_table(index='traffic_category', values='visits_quantity', aggfunc='sum').reset_index()
    
    df_pivot = df_pivot.to_dict('record')

    return df_pivot


def elitewheels_msk(df):
    elitewheels_categories_aliases = pd.read_csv(f'{FOLDER_PATH}/ew_msk_categories_aliases.csv')
    elitewheels_products_aliases = pd.read_csv(f'{FOLDER_PATH}/ew_msk_products_aliases.csv')
    elitewheels_filters_aliases = pd.read_csv(f'{FOLDER_PATH}/ew_msk_filters_aliases.csv')

    main = 'https://moscow.elitewheels.ru/'
    
    df['traffic_category'] = ''
    df['splitted_url'] = df['urls'].apply(lambda x: x.split('/'))
    df['only_alias'] = df['splitted_url'].apply(lambda x: x[len(x)-1])
    
    df.loc[df['urls'] == main, 'traffic_category'] = 'Главная'
    
    df.loc[df['only_alias'].isin(elitewheels_categories_aliases['alias']), 'traffic_category'] = 'Категории'
    df.loc[df['only_alias'].isin(elitewheels_products_aliases['alias']), 'traffic_category'] = 'Карточки'
    df.loc[df['only_alias'].isin(elitewheels_filters_aliases['alias']), 'traffic_category'] = 'Фильтры'

    df['traffic_category'] = df['traffic_category'].replace('', 'Другое')

    df.sort_values(by = 'visits_quantity', ascending = False, inplace = True) 

    df_pivot = df.pivot_table(index='traffic_category', values='visits_quantity', aggfunc='sum').reset_index()
    
    df_pivot = df_pivot.to_dict('record')

    return df_pivot


def kvp(df):
    kvp_categories_aliases = pd.read_csv(f'{FOLDER_PATH}/kvp_categories_aliases.csv')
    kvp_products_aliases = pd.read_csv(f'{FOLDER_PATH}/kvp_products_aliases.csv')
    kvp_filters_aliases = pd.read_csv(f'{FOLDER_PATH}/kvp_filters_aliases.csv')

    main = 'https://www.kolesa-v-pitere.ru/'
    
    df['traffic_category'] = ''
    df['splitted_url'] = df['urls'].apply(lambda x: x.split('/'))
    df['only_alias'] = df['splitted_url'].apply(lambda x: x[len(x)-1])
    
    df.loc[df['urls'] == main, 'traffic_category'] = 'Главная'
    
    df.loc[df['only_alias'].isin(kvp_categories_aliases['alias']), 'traffic_category'] = 'Категории'
    df.loc[df['only_alias'].isin(kvp_products_aliases['alias']), 'traffic_category'] = 'Карточки'
    df.loc[df['only_alias'].isin(kvp_filters_aliases['alias']), 'traffic_category'] = 'Фильтры'

    df['traffic_category'] = df['traffic_category'].replace('', 'Другое')

    df.sort_values(by = 'visits_quantity', ascending = False, inplace = True) 

    df_pivot = df.pivot_table(index='traffic_category', values='visits_quantity', aggfunc='sum').reset_index()
    
    df_pivot = df_pivot.to_dict('record')

    return df_pivot


def koleso(df):
    cat = df['urls'].str.contains(pat='https://the-koleso.ru/.*/$',regex=True)
    subdomain = df['urls'].str.contains(pat='https://.*[a-z].the-koleso.ru/.*',regex=True)

    koleso_products_aliases = pd.read_csv(f'{FOLDER_PATH}/koleso_products_aliases.csv')
    koleso_filters_aliases = pd.read_csv(f'{FOLDER_PATH}/koleso_filters_aliases.csv')

    main = 'https://the-koleso.ru/'
    
    df['traffic_category'] = ''
    df['splitted_url'] = df['urls'].apply(lambda x: x.split('/'))
    df['only_alias'] = df['splitted_url'].apply(lambda x: x[len(x)-1])
    
    df.loc[df['urls'] == main, 'traffic_category'] = 'Главная'
    
    df.loc[df['urls'].isin(df[cat]['urls']), 'traffic_category'] = 'Категории'
    df.loc[df['urls'].isin(df[subdomain]['urls']), 'traffic_category'] = 'Региональные поддомены'
    df.loc[df['only_alias'].isin(koleso_products_aliases['alias']), 'traffic_category'] = 'Карточки'
    df.loc[df['only_alias'].isin(koleso_filters_aliases['alias']), 'traffic_category'] = 'Фильтры'

    df['traffic_category'] = df['traffic_category'].replace('', 'Другое')

    df.sort_values(by = 'visits_quantity', ascending = False, inplace = True) 

    df_pivot = df.pivot_table(index='traffic_category', values='visits_quantity', aggfunc='sum').reset_index()
    
    df_pivot = df_pivot.to_dict('record')

    return df_pivot


def kypishiny(df):
    kypishiny_categories_aliases = pd.read_csv(f'{FOLDER_PATH}/ks_categories_aliases.csv')
    kypishiny_products_aliases = pd.read_csv(f'{FOLDER_PATH}/ks_products_aliases.csv')
    kypishiny_filters_aliases = pd.read_csv(f'{FOLDER_PATH}/ks_filters_aliases.csv')

    main = 'https://kypishiny.ru/'
    
    df['traffic_category'] = ''
    df['splitted_url'] = df['urls'].apply(lambda x: x.split('/'))
    df['only_alias'] = df['splitted_url'].apply(lambda x: x[len(x)-2])
    
    df.loc[df['urls'] == main, 'traffic_category'] = 'Главная'
    
    df.loc[df['only_alias'].isin(kypishiny_categories_aliases['alias']), 'traffic_category'] = 'Категории'
    df.loc[df['only_alias'].isin(kypishiny_products_aliases['alias']), 'traffic_category'] = 'Карточки'
    df.loc[df['only_alias'].isin(kypishiny_filters_aliases['alias']), 'traffic_category'] = 'Фильтры'

    df['traffic_category'] = df['traffic_category'].replace('', 'Другое')

    df.sort_values(by = 'visits_quantity', ascending = False, inplace = True) 

    df_pivot = df.pivot_table(index='traffic_category', values='visits_quantity', aggfunc='sum').reset_index()
    
    df_pivot = df_pivot.to_dict('record')

    return df_pivot


