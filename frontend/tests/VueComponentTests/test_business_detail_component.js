import { shallowMount } from '@vue/test-utils';
import axios from 'axios';
import BusinessDetail from '@/vue_components/business_detail.vue';
jest.mock('axios');

describe('BusinessDetail.vue', () => {
  let wrapper;
  const businessId = '1';
  const mockBusinessData = {
    id: businessId,
    name: 'Test Business',
    description: 'This is a test business'
  };

  beforeEach(() => {
    wrapper = shallowMount(BusinessDetail, {
      mocks: {
        $route: {
          params: { id: businessId }
        }
      }
    });
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  it('fetches business details on component creation', async () => {
    axios.get.mockResolvedValueOnce({ data: mockBusinessData });
    await wrapper.vm.$nextTick();
    expect(axios.get).toHaveBeenCalledWith(`/api/businesses/${businessId}`);
    expect(wrapper.vm.business).toEqual(mockBusinessData);
  });

  it('handles error when fetching business details', async () => {
    const errorMessage = 'Failed to fetch business details';
    axios.get.mockRejectedValueOnce(new Error(errorMessage));
    global.alert = jest.fn();
    await wrapper.vm.$nextTick();
    expect(global.alert).toHaveBeenCalledWith(
      'An error occurred while fetching the business details.'
    );
  });

  it('updates business details', async () => {
    const updatedBusinessData = {
      name: 'Updated Business Name',
      description: 'Updated Business Description'
    };
    wrapper.setData({ business: updatedBusinessData });
    axios.post.mockResolvedValueOnce({ data: { message: 'Business updated successfully' } });
    global.alert = jest.fn();
    await wrapper.vm.updateBusiness();
    expect(axios.post).toHaveBeenCalledWith('/update_form', updatedBusinessData);
    expect(global.alert).toHaveBeenCalledWith('Business updated successfully');
  });

  it('handles error when updating business details', async () => {
    const updatedBusinessData = {
      name: 'Updated Business Name',
      description: 'Updated Business Description'
    };
    wrapper.setData({ business: updatedBusinessData });
    const errorMessage = 'Failed to update business details';
    axios.post.mockRejectedValueOnce(new Error(errorMessage));
    global.alert = jest.fn();
    await wrapper.vm.updateBusiness();
    expect(axios.post).toHaveBeenCalledWith('/update_form', updatedBusinessData);
    expect(global.alert).toHaveBeenCalledWith('An error occurred while updating the business.');
  });
});
