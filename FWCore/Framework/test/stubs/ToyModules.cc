
/*----------------------------------------------------------------------

Toy EDProducers and EDProducts for testing purposes only.

----------------------------------------------------------------------*/

#include "DataFormats/Common/interface/DetSetVector.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/RefProd.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/TestObjects/interface/ToyProducts.h"

#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/global/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include <cassert>
#include <stdexcept>
#include <string>
#include <vector>

namespace edmtest {

  //--------------------------------------------------------------------
  //
  // Toy producers
  //
  //--------------------------------------------------------------------

  //--------------------------------------------------------------------
  //
  // Produces and SCSimpleProduct product instance.
  //
  class SCSimpleProducer : public edm::stream::EDProducer<> {
  public:
    explicit SCSimpleProducer(edm::ParameterSet const& p) : size_(p.getParameter<int>("size")) {
      produces<SCSimpleProduct>();
      assert(size_ > 1);
    }

    explicit SCSimpleProducer(int i) : size_(i) {
      produces<SCSimpleProduct>();
      assert(size_ > 1);
    }

    virtual ~SCSimpleProducer() {}
    virtual void produce(edm::Event& e, edm::EventSetup const& c) override;

  private:
    int size_;  // number of Simples to put in the collection
  };

  void SCSimpleProducer::produce(edm::Event& e, edm::EventSetup const& /* unused */) {
    // Fill up a collection so that it is sorted *backwards*.
    std::vector<Simple> guts(size_);
    for (int i = 0; i < size_; ++i) {
      guts[i].key = size_ - i;
      guts[i].value = 1.5 * i;
    }

    // Verify that the vector is not sorted -- in fact, it is sorted
    // backwards!
    for (int i = 1; i < size_; ++i) {
      assert(guts[i - 1].id() > guts[i].id());
    }

    // Put the product into the Event, thus sorting it.
    e.put(std::make_unique<SCSimpleProduct>(guts));
  }

  //--------------------------------------------------------------------
  //
  // Produces and OVSimpleProduct product instance.
  //
  class OVSimpleProducer : public edm::stream::EDProducer<> {
  public:
    explicit OVSimpleProducer(edm::ParameterSet const& p) : size_(p.getParameter<int>("size")) {
      produces<OVSimpleProduct>();
      produces<OVSimpleDerivedProduct>("derived");
      assert(size_ > 1);
    }

    explicit OVSimpleProducer(int i) : size_(i) {
      produces<OVSimpleProduct>();
      produces<OVSimpleDerivedProduct>("derived");
      assert(size_ > 1);
    }

    virtual ~OVSimpleProducer() {}
    virtual void produce(edm::Event& e, edm::EventSetup const& c) override;

  private:
    int size_;  // number of Simples to put in the collection
  };

  void OVSimpleProducer::produce(edm::Event& e, edm::EventSetup const& /* unused */) {
    // Fill up a collection
    auto p = std::make_unique<OVSimpleProduct>();

    for (int i = 0; i < size_; ++i) {
      auto simple = std::make_unique<Simple>();
      simple->key = size_ - i;
      simple->value = 1.5 * i;
      p->push_back(std::move(simple));
    }

    // Put the product into the Event
    e.put(std::move(p));

    // Fill up a collection of SimpleDerived objects
    auto pd = std::make_unique<OVSimpleDerivedProduct>();

    for (int i = 0; i < size_; ++i) {
      auto simpleDerived = std::make_unique<SimpleDerived>();
      simpleDerived->key = size_ - i;
      simpleDerived->value = 1.5 * i + 100.0;
      simpleDerived->dummy = 0.0;
      pd->push_back(std::move(simpleDerived));
    }

    // Put the product into the Event
    e.put(std::move(pd), "derived");
  }

  //--------------------------------------------------------------------
  //
  // Produces and OVSimpleProduct product instance.
  //
  class VSimpleProducer : public edm::stream::EDProducer<> {
  public:
    explicit VSimpleProducer(edm::ParameterSet const& p) : size_(p.getParameter<int>("size")) {
      produces<VSimpleProduct>();
      assert(size_ > 1);
    }

    explicit VSimpleProducer(int i) : size_(i) {
      produces<VSimpleProduct>();
      assert(size_ > 1);
    }

    virtual ~VSimpleProducer() {}
    virtual void produce(edm::Event& e, edm::EventSetup const& c) override;

  private:
    int size_;  // number of Simples to put in the collection
  };

  void VSimpleProducer::produce(edm::Event& e, edm::EventSetup const& /* unused */) {
    // Fill up a collection
    auto p = std::make_unique<VSimpleProduct>();

    for (int i = 0; i < size_; ++i) {
      Simple simple;
      simple.key = size_ - i;
      simple.value = 1.5 * i + e.id().event();
      p->push_back(simple);
    }

    // Put the product into the Event
    e.put(std::move(p));
  }

  //--------------------------------------------------------------------
  //
  // Produces AssociationVector<vector<Simple>, vector<Simple> > object
  // This is used to test a View of an AssociationVector
  //
  class AVSimpleProducer : public edm::stream::EDProducer<> {
  public:
    explicit AVSimpleProducer(edm::ParameterSet const& p) : src_(p.getParameter<edm::InputTag>("src")) {
      produces<AVSimpleProduct>();
      consumes<std::vector<edmtest::Simple>>(src_);
    }

    virtual void produce(edm::Event& e, edm::EventSetup const& c) override;

  private:
    edm::InputTag src_;
  };

  void AVSimpleProducer::produce(edm::Event& e, edm::EventSetup const& /* unused */) {
    edm::Handle<std::vector<edmtest::Simple>> vs;
    e.getByLabel(src_, vs);
    // Fill up a collection
    auto p = std::make_unique<AVSimpleProduct>(edm::RefProd<std::vector<edmtest::Simple>>(vs));

    for (unsigned int i = 0; i < vs->size(); ++i) {
      edmtest::Simple simple;
      simple.key = 100 + i;  // just some arbitrary number for testing
      simple.value = .1 * e.id().event();
      p->setValue(i, simple);
    }

    // Put the product into the Event
    e.put(std::move(p));
  }

  //--------------------------------------------------------------------
  //
  // Produces two products:
  //    DSVSimpleProduct
  //    DSVWeirdProduct
  //
  class DSVProducer : public edm::stream::EDProducer<> {
  public:
    explicit DSVProducer(edm::ParameterSet const& p) : size_(p.getParameter<int>("size")) {
      produces<DSVSimpleProduct>();
      produces<DSVWeirdProduct>();
      assert(size_ > 1);
    }

    explicit DSVProducer(int i) : size_(i) {
      produces<DSVSimpleProduct>();
      produces<DSVWeirdProduct>();
      assert(size_ > 1);
    }

    virtual ~DSVProducer() {}

    virtual void produce(edm::Event& e, edm::EventSetup const&) override;

  private:
    template <typename PROD>
    void make_a_product(edm::Event& e);
    int size_;
  };

  void DSVProducer::produce(edm::Event& e, edm::EventSetup const& /* unused */) {
    this->make_a_product<DSVSimpleProduct>(e);
    this->make_a_product<DSVWeirdProduct>(e);
  }

  template <typename PROD>
  void DSVProducer::make_a_product(edm::Event& e) {
    typedef PROD product_type;
    typedef typename product_type::value_type detset;
    typedef typename detset::value_type value_type;

    // Fill up a collection so that it is sorted *backwards*.
    std::vector<value_type> guts(size_);
    for (int i = 0; i < size_; ++i) {
      guts[i].data = size_ - i;
    }

    // Verify that the vector is not sorted -- in fact, it is sorted
    // backwards!
    for (int i = 1; i < size_; ++i) {
      assert(guts[i - 1].data > guts[i].data);
    }

    auto p = std::make_unique<product_type>();
    int n = 0;
    for (int id = 1; id < size_; ++id) {
      ++n;
      detset item(id);  // this will get DetID id
      item.data.insert(item.data.end(), guts.begin(), guts.begin() + n);
      p->insert(item);
    }

    // Put the product into the Event, thus sorting it ... or not,
    // depending upon the product type.
    e.put(std::move(p));
  }

  //--------------------------------------------------------------------
  //
  // Produces two products: (new DataSetVector)
  //    DSTVSimpleProduct
  //    DSTVSimpleDerivedProduct
  //
  class DSTVProducer : public edm::stream::EDProducer<> {
  public:
    explicit DSTVProducer(edm::ParameterSet const& p) : size_(p.getParameter<int>("size")) {
      produces<DSTVSimpleProduct>();
      produces<DSTVSimpleDerivedProduct>();
      assert(size_ > 1);
    }

    explicit DSTVProducer(int i) : size_(i) {
      produces<DSTVSimpleProduct>();
      produces<DSTVSimpleDerivedProduct>();
      assert(size_ > 1);
    }

    virtual ~DSTVProducer() {}

    virtual void produce(edm::Event& e, edm::EventSetup const&) override;

  private:
    template <typename PROD>
    void make_a_product(edm::Event& e);
    void fill_a_data(DSTVSimpleProduct::data_type& d, unsigned int i);
    void fill_a_data(DSTVSimpleDerivedProduct::data_type& d, unsigned int i);

    int size_;
  };

  void DSTVProducer::produce(edm::Event& e, edm::EventSetup const& /* unused */) {
    this->make_a_product<DSTVSimpleProduct>(e);
    this->make_a_product<DSTVSimpleDerivedProduct>(e);
  }

  void DSTVProducer::fill_a_data(DSTVSimpleDerivedProduct::data_type& d, unsigned int i) {
    d.key = size_ - i;
    d.value = 1.5 * i;
  }

  void DSTVProducer::fill_a_data(DSTVSimpleProduct::data_type& d, unsigned int i) { d.data = size_ - i; }

  template <typename PROD>
  void DSTVProducer::make_a_product(edm::Event& e) {
    typedef PROD product_type;
    //FIXME
    typedef typename product_type::FastFiller detset;
    typedef typename detset::id_type id_type;

    auto p = std::make_unique<product_type>();
    product_type& v = *p;

    unsigned int n = 0;
    for (id_type id = 1; id < static_cast<id_type>(size_); ++id) {
      ++n;
      detset item(v, id);  // this will get DetID id
      item.resize(n);
      for (unsigned int i = 0; i < n; ++i)
        fill_a_data(item[i], i);
    }

    // Put the product into the Event, thus sorting is not done by magic,
    // up to one user-line
    e.put(std::move(p));
  }

  //--------------------------------------------------------------------
  //
  // Produces an Prodigal instance.
  //
  class ProdigalProducer : public edm::stream::EDProducer<> {
  public:
    explicit ProdigalProducer(edm::ParameterSet const& p) : label_(p.getParameter<std::string>("label")) {
      produces<Prodigal>();
      consumes<IntProduct>(edm::InputTag{label_});
    }
    virtual ~ProdigalProducer() {}
    virtual void produce(edm::Event& e, edm::EventSetup const& c) override;

  private:
    std::string label_;
  };

  void ProdigalProducer::produce(edm::Event& e, edm::EventSetup const&) {
    // EventSetup is not used.

    // The purpose of Prodigal is testing of *not* keeping
    // parentage. So we need to get a product...
    edm::Handle<IntProduct> parent;
    e.getByLabel(label_, parent);

    e.put(std::make_unique<Prodigal>(parent->value));
  }

  class IntProductFilter : public edm::global::EDFilter<> {
  public:
    explicit IntProductFilter(edm::ParameterSet const& p)
        : token_(consumes(p.getParameter<edm::InputTag>("label"))),
          threshold_(p.getParameter<int>("threshold")),
          shouldProduce_(p.getParameter<bool>("shouldProduce")) {
      if (shouldProduce_) {
        putToken_ = produces<edmtest::IntProduct>();
      }
    }

    bool filter(edm::StreamID, edm::Event& iEvent, edm::EventSetup const&) const {
      auto const& product = iEvent.get(token_);
      if (product.value < threshold_) {
        return false;
      }
      iEvent.emplace(putToken_, product);
      return true;
    }

    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
      edm::ParameterSetDescription desc;
      desc.add<edm::InputTag>("label");
      desc.add<int>("threshold", 0);
      desc.add<bool>("shouldProduce", false);
      descriptions.addDefault(desc);
    }

  private:
    const edm::EDGetTokenT<edmtest::IntProduct> token_;
    edm::EDPutTokenT<edmtest::IntProduct> putToken_;
    const int threshold_;
    const bool shouldProduce_;
  };

}  // namespace edmtest

using edmtest::AVSimpleProducer;
using edmtest::DSTVProducer;
using edmtest::DSVProducer;
using edmtest::IntProductFilter;
using edmtest::OVSimpleProducer;
using edmtest::ProdigalProducer;
using edmtest::SCSimpleProducer;
using edmtest::VSimpleProducer;
DEFINE_FWK_MODULE(SCSimpleProducer);
DEFINE_FWK_MODULE(OVSimpleProducer);
DEFINE_FWK_MODULE(VSimpleProducer);
DEFINE_FWK_MODULE(AVSimpleProducer);
DEFINE_FWK_MODULE(DSVProducer);
DEFINE_FWK_MODULE(DSTVProducer);
DEFINE_FWK_MODULE(ProdigalProducer);
DEFINE_FWK_MODULE(IntProductFilter);
