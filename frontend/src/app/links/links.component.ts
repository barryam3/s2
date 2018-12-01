import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { Observable, Subscription } from 'rxjs';

import { Song } from '../song.service';
import { LinkService, Link } from '../link.service';
import { filterInPlace } from '../../utils';

@Component({
  selector: 'app-links',
  templateUrl: './links.component.html',
  styleUrls: ['./links.component.scss'],
})
export class LinksComponent implements OnInit, OnDestroy {
  @Input() song: Song;
  @Input() showEdit = false;
  @Input() commitEvents: Observable<void>;
  @Input() cancelEvents: Observable<void>;

  newLinkURL = '';
  newLinkDescription = '';
  tempLinkID = -1;
  idsToDelete: Set<number> = new Set();
  linksToCreate: Link[] = [];

  commitSubscription: Subscription;
  cancelSubscription: Subscription;

  ngOnInit() {
    this.commitSubscription = this.commitEvents.subscribe(this.commitChanges);
    this.cancelSubscription = this.cancelEvents.subscribe(this.cancelChanges);
  }

  ngOnDestroy() {
    this.commitSubscription.unsubscribe();
    this.cancelSubscription.unsubscribe();
  }

  constructor(private linkService: LinkService) { }

  get links() {
    return [...this.song.links, ...this.linksToCreate].filter(({ id }) => !this.idsToDelete.has(id));
  }

  deleteLink(linkID: number) {
    this.idsToDelete.add(linkID);
  }

  addLink() {
    this.linksToCreate.push({
      // links need unique ids
      // the database does not use negative ids
      id: this.tempLinkID,
      url: this.newLinkURL,
      description: this.newLinkDescription,
    });
    this.tempLinkID -= 1;
    this.newLinkURL = '';
    this.newLinkDescription = '';
  }

  commitChanges = () => {
    this.linksToCreate.forEach(({ url, description }) => {
      this.linkService.addLink(this.song.id, realURL, description)
        .subscribe(newLink =>  this.song.links.push(newLink));
    });
    this.idsToDelete.forEach(id => {
      this.linkService.deleteLink(id).subscribe(() => {
        filterInPlace(this.song.links, link => link.id !== id);
      });
    });
    this.linksToCreate = [];
    this.idsToDelete = new Set();
  }

  cancelChanges = () => {
    this.linksToCreate = [];
    this.idsToDelete = new Set();
  }

}
