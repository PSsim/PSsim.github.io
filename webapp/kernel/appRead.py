
def fcn_Read(FileName):
    ############################################################
    def fcn_findidx(Data, row_start):
        idxini = -1
        idxfin = -1
        for k in range(row_start, len(Data)):
            # prevent a row being empty when it is asked below if it presents a digit
            if len(Data[k]) == 0:
                Data[k] = 'hello'
            if Data[k][0].isdigit() and idxini == -1:
                idxini = k
            if (Data[k][0].isdigit() == False and idxini != -1 and idxfin == -1):
                idxfin = k
                break
            # to consider the case that the last row ends with a digit
            if k == len(Data)-1:
                idxfin = k+1
        Data_string = '\n'.join(Data[idxini:idxfin])
        output = [Data_string, idxfin-idxini]
        return output, idxfin
    # ------------------------

    # ------------------------
    with open('kernel/' + FileName + '.txt', 'r') as file:
        FullStringData = file.read()
    # ------------------------
    Data = FullStringData.split(sep='\n')
    # ------------------------
    LNdata, idxfinLN = fcn_findidx(Data, 0)
    SHdata, idxfinSH = fcn_findidx(Data, idxfinLN)
    SWdata, idxfinSW = fcn_findidx(Data, idxfinSH)
    PVdata, idxfinPV = fcn_findidx(Data, idxfinSW)
    PQdata,        _ = fcn_findidx(Data, idxfinPV)
    ############################################################
    return LNdata, SHdata, SWdata, PVdata, PQdata
