import { shallowMount } from '@vue/test-utils';
import axios from 'axios';
import SpecialOffer from '@/vue_components/special_offer.vue';
jest.mock('axios');

describe('SpecialOffer.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(SpecialOffer);
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  it('submits form for new offer', async () => {
    const offerData = {
      title: 'Test Title',
      description: 'Test Description',
      expiration_date: '2022-12-31',
      associated_business: 'Test Business'
    };
    axios.post.mockResolvedValue({ data: offerData });
    wrapper.setData({ offer: offerData });
    await wrapper.vm.submitForm();
    expect(axios.post).toHaveBeenCalledWith('/offers', offerData);
  });

  it('submits form for updating offer', async () => {
    const offerData = {
      title: 'Test Title',
      description: 'Test Description',
      expiration_date: '2022-12-31',
      associated_business: 'Test Business'
    };
    axios.put.mockResolvedValue({ data: offerData });
    wrapper.setData({ offer: offerData, offerId: 1 });
    await wrapper.vm.submitForm();
    expect(axios.put).toHaveBeenCalledWith('/offers/1', offerData);
  });

  it('deletes offer', async () => {
    axios.delete.mockResolvedValue({});
    wrapper.setData({ offerId: 1 });
    await wrapper.vm.deleteOffer();
    expect(axios.delete).toHaveBeenCalledWith('/offers/1');
  });

  it('fetches offer on creation if offerId exists', async () => {
    const offerData = {
      title: 'Test Title',
      description: 'Test Description',
      expiration_date: '2022-12-31',
      associated_business: 'Test Business'
    };
    axios.get.mockResolvedValue({ data: offerData });
    wrapper = shallowMount(SpecialOffer, {
      data() {
        return { offerId: 1 };
      }
    });
    await wrapper.vm.$nextTick();
    expect(axios.get).toHaveBeenCalledWith('/offers/1');
    expect(wrapper.vm.offer).toEqual(offerData);
  });

  it('handles errors when submitting a new offer', async () => {
    const offerData = {
      title: 'Test Title',
      description: 'Test Description',
      expiration_date: '2022-12-31',
      associated_business: 'Test Business'
    };
    const error = new Error('Error submitting offer');
    axios.post.mockRejectedValue(error);
    wrapper.setData({ offer: offerData });
    await wrapper.vm.submitForm();
    expect(axios.post).toHaveBeenCalledWith('/offers', offerData);
    expect(console.error).toHaveBeenCalledWith(error);
  });

  it('handles errors when updating an offer', async () => {
    const offerData = {
      title: 'Test Title',
      description: 'Test Description',
      expiration_date: '2022-12-31',
      associated_business: 'Test Business'
    };
    const error = new Error('Error updating offer');
    axios.put.mockRejectedValue(error);
    wrapper.setData({ offer: offerData, offerId: 1 });
    await wrapper.vm.submitForm();
    expect(axios.put).toHaveBeenCalledWith('/offers/1', offerData);
    expect(console.error).toHaveBeenCalledWith(error);
  });

  it('handles errors when deleting an offer', async () => {
    const error = new Error('Error deleting offer');
    axios.delete.mockRejectedValue(error);
    wrapper.setData({ offerId: 1 });
    await wrapper.vm.deleteOffer();
    expect(axios.delete).toHaveBeenCalledWith('/offers/1');
    expect(console.error).toHaveBeenCalledWith(error);
  });
    
  it('handles errors when fetching an offer', async () => {
    const error = new Error('Error fetching offer');
    axios.get.mockRejectedValue(error);
    wrapper = shallowMount(SpecialOffer, {
      data() {
        return { offerId: 1 };
      }
    });
    await wrapper.vm.$nextTick();
    expect(axios.get).toHaveBeenCalledWith('/offers/1');
    expect(console.error).toHaveBeenCalledWith(error);
  });
  
  it('does not fetch offer on creation if offerId does not exist', async () => {
    wrapper = shallowMount(SpecialOffer);
    await wrapper.vm.$nextTick();
    expect(axios.get).not.toHaveBeenCalled();
  });
  
  it('validates form inputs', async () => {
    wrapper = shallowMount(SpecialOffer);
    await wrapper.find('form').trigger('submit.prevent');
    expect(wrapper.find('input[required]').element.validity.valueMissing).toBe(true);
    expect(wrapper.find('textarea[required]').element.validity.valueMissing).toBe(true);
  });})