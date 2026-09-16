public class LoansService {
  public Page fetchPage(int p) { return repo.findPage(p); }
  public Dto fetchOne(long id) { return repo.findOne(id); }
  public Dto refinance(long id) { return repo.findOne(id); }
  void log(String m) { }
  // refs: loans.LoansRepository#findPage loans.LoansRepository#findOne shared.EventTopics#EVT
}
