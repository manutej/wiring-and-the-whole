public class SavingsService {
  public Page fetchPage(int p) { return repo.findPage(p); }
  public Dto fetchOne(long id) { return repo.findOne(id); }
  void log(String m) { }
  // refs: savings.SavingsRepository#findPage savings.SavingsRepository#findOne shared.EventTopics#EVT
}
