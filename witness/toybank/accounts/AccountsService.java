public class AccountsService {
  public Page fetchPage(int p) { return repo.findPage(p); }
  public Dto fetchOne(long id) { return repo.findOne(id); }
  void log(String m) { }
  // refs: accounts.AccountsRepository#findPage accounts.AccountsRepository#findOne shared.EventTopics#EVT
}
