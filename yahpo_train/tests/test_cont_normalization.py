import torch
import numpy as np
from yahpo_train.cont_normalization import ContNormalization
import pandas as pd
import pytest

def test_cont_norm():
    xss = [
        torch.rand(100,1),
        (torch.rand(1000,1) * 3) ** 2,
        -  5 * (torch.rand(500, 1) -.5),
        (torch.rand(500, 1) + 2) ** 3,
        torch.cat((torch.rand(500, 1), torch.rand(1,1) + torch.Tensor([1000.]))),
        torch.Tensor([1., 2., -1., 100000])
    ]
    xs2 = torch.cat((torch.rand(50, 1), torch.rand(1,1) + torch.Tensor([10000.]), torch.Tensor([-1000.]).unsqueeze(1)))
    for xs in xss:
        for normalize in ["scale", "range", None]:
            tfm = ContNormalization(xs, normalize = normalize)
            xt = tfm(xs)
            xsn = tfm.invert(xt)            
            assert torch.mean(torch.abs(xsn - xs)) / torch.max(xs) < 1e-4
            assert xsn.shape == xs.shape

            # New data
            xt2 = tfm(xs2)
            xsn2 = tfm.invert(xt2)
            assert torch.mean(torch.abs(xsn2 - xs2)) / torch.max(xs2) < 1e-4
            assert xsn2.shape == xs2.shape

def test_cont_norm_pd():
    nrows = 1000000
    df2 = pd.read_csv("/home/flo/lrz_synchshare/multifidelity_data/lcbench/data.csv", nrows=nrows).sample(frac=.01)
    df = pd.read_csv("/home/flo/lrz_synchshare/multifidelity_data/lcbench/data.csv").sample(frac = .3)
    for nm in df.columns[1:]:
        # print(nm)
        for normalize in ["scale", "range", None]:
            xs = torch.Tensor(df[nm].values)
            tfm = ContNormalization(xs, normalize = normalize)
            xt = tfm(xs)
            xsn = tfm.invert(xt)
            assert torch.mean(torch.abs(xsn - xs)) / torch.max(xs) < 1e-4
            assert xsn.shape == xs.shape
            assert tfm.lmbda <= tfm.lmbda <= 5.1
            xs = torch.Tensor(df2[nm].values)
            xt = tfm(xs)
            xsn = tfm.invert(xt)
            assert torch.mean(torch.abs(xsn - xs)) / torch.max(xs) < 1e-4
            assert xsn.shape == xs.shape

if __name__ == '__main__':
    test_cont_norm()
    test_cont_norm_pd()