if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    
    data.columns = (data.columns
                    .str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True)
                    .str.lower()
    )

    data["lpep_pickup_date"] = data["lpep_pickup_datetime"].dt.date

    data = data[data['passenger_count'] > 0]
    data = data[data['trip_distance'] > 0]

    return data

    
@test
def test_output(output, *args):
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers'
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are trip_distance equal to zero'
    assert 'vendor_id' in output.columns, 'There are not vendor_id column'
    