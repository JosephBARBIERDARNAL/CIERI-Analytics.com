import pandas as pd
pd.set_option('future.no_silent_downcasting', True)


class SHARE:


    def __init__(self, mainDirectory: str, verbose: bool=True) -> None:
        self.mainDirectory = mainDirectory
        self.hasData = False
        self.verbose = verbose
        self.data = pd.DataFrame()
        self.waveToYear =  {
            1: 2004,
            2: 2006,
            3: 2008,
            4: 2011,
            5: 2013,
            6: 2015,
            7: 2017,
            8: 2019
        }


    def getDataset(self, wave: int, varList: list, autoClean=True) -> pd.DataFrame:
        if autoClean:
            varList.append('dn003_')
        self.varList = varList
        df = self.data
        
        # check if the data is already loaded
        if self.hasData:
            if set(varList).issubset(set(df.columns)):
                if self.verbose:
                    print('Data is already loaded')
                return df[varList]
            
        # open and merge the datasets
        varSuffix = list(set([var[:2] for var in varList]))
        for suffix in varSuffix:
            path = f'{self.mainDirectory}/sharew{wave}_rel8-0-0_ALL_datasets_stata/sharew{wave}_rel8-0-0_{suffix}.dta'
            data = pd.read_stata(path)
            if not df.empty:
                df = pd.merge(df, data, on='mergeid', how='outer')
            else:
                df = data
        df = df[varList+['country', 'mergeid']]
        df = df.loc[:,~df.columns.duplicated()]
        
        # apply simple cleaning
        if autoClean:
            df = self.transformNans(df)
            year = self.waveToYear[wave]
            df['dn003_'] = df['dn003_'].astype(float)
            df['Age'] = year - df['dn003_']
            df = df.loc[df['Age'] >= 50,]

        self.data = df
        self.hasData = True
        return df
            

    def transformNans(self, df: pd.DataFrame) -> pd.DataFrame:
        valuesToReplace = ["Don't know", "Refusal",
                     "Implausible value/suspected wrong", 
                     "Not codable", "Not answered",
                     "Not yet coded", "Not applicable"]
        df = df.replace(valuesToReplace, pd.NA)
        self.data = df
        return df
    

    def transformDummies(self, df: pd.DataFrame) -> pd.DataFrame:

        # transform categorical variables to dummies
        varToDummy = []
        for var in df.columns:
            if var in ['country', 'mergeid']:
                pass
            else:
                try:
                    df[var] = df[var].astype(float)
                except ValueError:
                    df[var] = df[var].astype(str)
                    varToDummy.append(var)
        df = pd.get_dummies(df, columns=varToDummy, drop_first=True)

        # transform boolean columns to int
        boolColumns = df.select_dtypes(include='bool').columns
        for col in boolColumns:
            df[col] = df[col].astype(int)

        self.varToDummy = varToDummy
        self.data = df
        return df
