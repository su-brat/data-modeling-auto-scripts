import pandas as pd

INPUT_DM_SHEET = './backup/Catalyst_alpha_dm_tag_mapping.xlsx'
INPUT_COMP_STYLE_SHEET = './Catalyst_component_style.xlsx'
OUTPUT_DM_SHEET = 'Catalyst_alpha_filled_dm_tag_mapping.csv'

def getcompstyle(xpaths, compstylemap):
    '''
    compstylemap = {
        'concept': {'Component': 'section', 'Style': 'TRContentLevel', 'HasLevel': 'yes'}
    }
    '''
    complist = []
    stylelist = []
    xpathcompmap = {}
    '''
    xpathcompmap = {
        '/book/concept/': {'Component': 'section', 'Style': 'TRContentLevel', 'Level': 1}
    }
    '''
    for xpath in xpaths:
        tag = xpath.split('/')[-1]
        parentxpath = '/'.join(xpath.strip().split('/')[:-1])
        if tag in compstylemap:
            comp = compstylemap[tag]['Component']
            style = compstylemap[tag]['Style']
            if comp == 'paragraph':
                parentcomp = xpathcompmap[parentxpath]['Component']
                if parentcomp!='section':
                    comp = parentcomp
                    style = xpathcompmap[parentxpath]['Style']
            level = xpathcompmap[parentxpath].get('Level', 0) if parentxpath in xpathcompmap else 0
            if compstylemap[tag]['HasLevel']=='yes':
                level += 1
        elif parentxpath in xpathcompmap:
            comp = xpathcompmap[parentxpath]['Component']
            style = xpathcompmap[parentxpath]['Style']
            level = xpathcompmap[parentxpath].get('Level', 0)
        else:
            comp = ''
            style = ''
            level = 0
        
        xpathcompmap[xpath] = {'Component': comp, 'Style': style, 'Level': level}
        complist.append(comp)
        if 'Level' not in style:
            level = ''
        else:
            level = str(level)
        stylelist.append(style+level)

    return complist, stylelist

if __name__ == '__main__':
    print('Reading DM tag mapping sheet...')
    df = pd.read_excel(INPUT_DM_SHEET)
    xpaths = df['Legacy Xpaths'].to_list()
    print('Reading Component & style sheet...')
    compstyledf = pd.read_excel(INPUT_COMP_STYLE_SHEET)
    tbl = compstyledf.to_dict('list')
    print('Computing Components and styles...')
    n = len(tbl['LegacyTag'])
    compstylemap = {}
    for i in range(n):
        for legacytag in tbl['LegacyTag'][i].split(','):
            compstylemap[legacytag] = {'Component': tbl['Component'][i], 'Style': tbl['Style'][i], 'HasLevel': tbl['HasLevel'][i]}
    components, styles = getcompstyle(xpaths=xpaths, compstylemap=compstylemap)
    print('Dumping output to file...')
    out_df = pd.DataFrame.from_dict({'Legacy Xpaths': xpaths, 'Components': components, 'Styles': styles})
    out_df.to_csv(OUTPUT_DM_SHEET)
    print('Generated filled mapping sheet')
